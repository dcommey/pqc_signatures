import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path

class PQCVisualizer:
    def __init__(self, results_path='results/pqc_blockchain_benchmarks.json'):
        with open(results_path) as f:
            self.results = json.load(f)
            
        plt.style.use('seaborn-v0_8-paper')
        sns.set_context("paper", font_scale=1.5)
        self.colors = sns.color_palette("deep")
        
    def _format_size(self, size_bytes):
        for unit in ['B', 'KB', 'MB']:
            if size_bytes < 1024:
                return f"{size_bytes:.0f}{unit}"
            size_bytes /= 1024
        return f"{size_bytes:.0f}MB"

    def create_comparison_plot(self):
        plt.figure(figsize=(12, 6))
        scheme_names = list(self.results.keys())
        
        # Prepare data
        pure_times = []
        blockchain_times = []
        message_sizes = []
        schemes = []
        
        for scheme_name, scheme_data in self.results.items():
            for key, measurement in scheme_data['measurements'].items():
                size = int(key.split('_')[-1])
                pure_times.append(measurement['pure_crypto']['pure_verification_time_ms'])
                blockchain_times.append(measurement['blockchain_overhead']['blockchain_verification_time_ms'])
                message_sizes.append(self._format_size(size))
                schemes.append(scheme_name)
        
        df = pd.DataFrame({
            'Message Size': message_sizes,
            'Scheme': schemes,
            'Pure Verification (ms)': pure_times,
            'Blockchain Verification (ms)': blockchain_times
        })
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        sns.barplot(data=df, x='Message Size', y='Pure Verification (ms)', 
                   hue='Scheme', ax=ax1)
        ax1.set_title('Pure Verification Time')
        ax1.tick_params(axis='x', rotation=45)
        
        sns.barplot(data=df, x='Message Size', y='Blockchain Verification (ms)', 
                   hue='Scheme', ax=ax2)
        ax2.set_title('Blockchain Verification Time')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('results/verification_comparison.pdf', dpi=300, bbox_inches='tight')
        plt.close()

    def create_gas_analysis_plot(self):
        scheme_names = []
        base_gas = []
        verify_gas = []
        sig_sizes = []
        
        for scheme_name, scheme_data in self.results.items():
            # Take measurements from middle message size
            mid_size_key = list(scheme_data['measurements'].keys())[2]
            measurement = scheme_data['measurements'][mid_size_key]
            
            scheme_names.append(scheme_name)
            base_gas.append(measurement['blockchain_overhead']['base_transaction_gas'])
            verify_gas.append(measurement['blockchain_overhead']['verification_gas'])
            sig_sizes.append(measurement['pure_crypto']['signature_size'])
        
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        # Plot stacked bars
        x = np.arange(len(scheme_names))
        width = 0.35
        
        ax1.bar(x, base_gas, width, label='Base Gas', color='lightblue')
        ax1.bar(x, verify_gas, width, bottom=base_gas, label='Verification Gas', color='darkblue')
        
        # Add signature size on secondary axis
        ax2 = ax1.twinx()
        ax2.plot(x, sig_sizes, 'r--', marker='o', label='Signature Size')
        
        # Set labels and legend
        ax1.set_xlabel('Scheme')
        ax1.set_ylabel('Gas Used')
        ax2.set_ylabel('Signature Size (bytes)')
        
        ax1.set_xticks(x)
        ax1.set_xticklabels(scheme_names)
        
        # Combine legends
        handles1, labels1 = ax1.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(handles1 + handles2, labels1 + labels2, loc='upper left')
        
        plt.title('Gas Usage and Signature Size Comparison')
        plt.tight_layout()
        plt.savefig('results/gas_analysis.pdf', dpi=300, bbox_inches='tight')
        plt.close()

    def create_latex_tables(self):
        # Table 1: Core Cryptographic Performance
        crypto_table = """\\begin{table}[h]
\\centering
\\caption{Core Cryptographic Performance Metrics}
\\label{tab:crypto_perf}
\\begin{tabular}{lcccc}
\\toprule
Scheme & Key Gen (ms) & Sign (ms) & Verify (ms) & Sig Size (B) \\\\
\\midrule
"""
        
        for scheme_name, scheme_data in self.results.items():
            mid_size_key = list(scheme_data['measurements'].keys())[2]
            measurement = scheme_data['measurements'][mid_size_key]['pure_crypto']
            
            crypto_table += f"{scheme_name} & "
            crypto_table += f"{measurement['key_generation_time_ms']:.2f} & "
            crypto_table += f"{measurement['signing_time_ms']:.2f} & "
            crypto_table += f"{measurement['pure_verification_time_ms']:.2f} & "
            crypto_table += f"{measurement['signature_size']} \\\\\n"
        
        crypto_table += """\\bottomrule
\\end{tabular}
\\end{table}
"""

        # Table 2: Blockchain Integration Overhead
        overhead_table = """\\begin{table}[h]
\\centering
\\caption{Blockchain Integration Overhead}
\\label{tab:blockchain_overhead}
\\begin{tabular}{lcccc}
\\toprule
Scheme & Verification & Gas & Gas/Byte & Overhead \\\\
& Time (ms) & Used & Ratio & Ratio \\\\
\\midrule
"""
        
        for scheme_name, scheme_data in self.results.items():
            mid_size_key = list(scheme_data['measurements'].keys())[2]
            measurement = scheme_data['measurements'][mid_size_key]
            
            overhead_table += f"{scheme_name} & "
            overhead_table += f"{measurement['blockchain_overhead']['blockchain_verification_time_ms']:.2f} & "
            overhead_table += f"{int(measurement['blockchain_overhead']['total_gas']):,} & "
            overhead_table += f"{measurement['blockchain_overhead']['gas_per_byte']:.1f} & "
            overhead_table += f"{measurement['blockchain_overhead']['verification_overhead_ratio']:.2f}x \\\\\n"
        
        overhead_table += """\\bottomrule
\\end{tabular}
\\end{table}
"""

        # Save tables
        with open('results/tables.tex', 'w') as f:
            f.write(crypto_table)
            f.write('\n')
            f.write(overhead_table)

def main():
    visualizer = PQCVisualizer()
    visualizer.create_comparison_plot()
    visualizer.create_gas_analysis_plot()
    visualizer.create_latex_tables()

if __name__ == "__main__":
    main()