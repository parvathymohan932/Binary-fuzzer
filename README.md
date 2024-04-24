# Fuzzing Programs with Structure-Aware Fuzzers

## Introduction
This repository introduces a generation-based structure-aware fuzzer that utilizes the format defined in Kaitai Struct. Additionally, we enhance structure-aware fuzzing in libFuzzer by integrating Kaitai Struct. Kaitai Struct’s capability to define complex data structures in a declarative manner makes it well-suited for use as input to our tool. This work addresses the limitations of traditional fuzzing methods by leveraging knowledge of the program’s structure to guide the generation of input data.

## Prerequisites
- Install Kaitai Struct. Refer to the documentation [here](https://doc.kaitai.io/user_guide.html).

## Usage of Generation Fuzzer
1. Setup Python.
2. Run the code.

## Installation of libFuzzer
- Refer to the documentation of libFuzzer [here](https://llvm.org/docs/LibFuzzer.html).
