# Fuzzing Programs with Structure-Aware Fuzzers

## Introduction
Ensuring software security and robustness is a persistent challenge, particularly in complex network systems such as Virtual Broadband Network Gateways (vBNGs). Fuzzing, a widely used software testing technique, helps identify vulnerabilities by subjecting a system to diverse test inputs and monitoring its behavior. However, its application in telecom systems presents challenges due to structured binary inputs, complex protocol interactions, and real-world constraints.

This project applies structure-aware fuzzing to a vBNG using Kaitai Struct, a declarative language for describing binary file formats. By leveraging protocol specifications, our fuzzer generates format-compliant test cases to explore vulnerabilities systematically. A specialized fuzzer bot analyzes responses and detects violations using a grammar-driven approach.

## Features
• Black-box Structure-Aware Fuzzing: Generates test cases that conform to protocol specifications.

• Kaitai Struct-Based Input Generation: Uses declarative specifications to ensure valid binary inputs.

• Grammar-Based Response Analysis: Identifies interesting test cases based on deviations from expected behavior.

• Mutation Strategies: Swaps equivalent packets in traces while maintaining protocol validity.

• Systematic Packet Sequence Exploration: Enhances security assessment by uncovering weaknesses in protocol implementations.

## Getting Started

### Prerequisites

• Python 3.8+

• Kaitai Struct Compiler

• A testing environment with vBNG access

### Installation & Execution

1. Clone the repository:
>   git clone https://github.com/parvathymohan932/Binary-fuzzer.git

2. Run the fuzzer bot and process test cases:
```
    cd fuzzer_grammar

    python3 fuzzer_bot_9_3.py
```
   This generates interesting test cases in the harvested_for_mutation folder.

3. Mutate the generated test cases:

>   python3 mutate_traces.py

4. Process the mutated test cases:

>    python3 mutated_traces_processing.py

   This step sends the mutated test cases while integrating them with the fuzzer bot.

5. The final set of interesting test cases will be stored in:

>    cd harvested_test_cases

## Running the Generation Fuzzer

If you only want to try the generation fuzzer, follow these steps:

1. Navigate to the fuzzer directory and run main.py:
   
```
    cd fuzzer

    cd generation_fuzzer

     python3 main.py
```
## License

This project is licensed under the MIT License. See the LICENSE file for details.

