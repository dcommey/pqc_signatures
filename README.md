# PQC Signature Scheme Comparison

This project benchmarks post-quantum digital signature schemes (Dilithium, Falcon, and SPHINCS+) using liboqs. It measures key generation, signing, and verification performance, as well as cryptographic artifact sizes.

## Schemes Compared

- **Dilithium2 (ML-DSA-65)**  
  Security Level: NIST Level 2

- **Falcon-padded-512**  
  Security Level: NIST Level 1+

- **SPHINCS+-SHA2-128s-simple**  
  Security Level: NIST Level 2

## Benchmarking Details

Metrics include:
- Execution time (ms) for key generation, signing, and verification.
- Signature, public key, and private key sizes.
- **Blockchain Integration Overhead** such as transaction gas costs and blockchain verification latency.

Results are saved in the `results/` directory:
- Detailed measurements: `results/detailed_measurements.json`
- Summary table: `results/summary.csv`
- Blockchain benchmarks: `results/pqc_blockchain_benchmarks.json` and PDF plots in `results/`

## Blockchain Integration

This project also benchmarks the integration of post-quantum schemes with blockchain verification. Using a deployed smart contract (e.g., PQCVerifier), the suite measures:
- Base transaction times and gas consumption.
- Additional overhead in blockchain-based signature verification.
- Gas usage per byte of signature data.

Ensure your local blockchain node is running (e.g., at http://127.0.0.1:8545) and that the smart contract is deployed with the correct ABI and address.

## Setup Instructions

1. Build liboqs with desired signature schemes enabled.
2. Set the library path, for example:  
   export LD_LIBRARY_PATH=~/liboqs/build/lib:$LD_LIBRARY_PATH
3. Create and activate a virtual environment.
4. Install the required Python dependencies:  
   pip install -r requirements.txt
5. Run benchmarks via:  
   python main.py  
   For blockchain tests, ensure your blockchain node and smart contract are correctly configured.

## License

MIT License
