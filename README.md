# B32K Concordance Ledger

A filesystem-first B32K research project for training a structural concordance from the King James Version of the Bible.

## Purpose

This project builds a machine-readable translation ledger for meaning-bearing structures.

The first corpus is the King James Version of the Bible.

The goal is not doctrinal enforcement, hidden-code numerology, or a claim that scripture secretly encodes modern physics. The goal is to build an agnostic structural concordance: a dataset that records how source images function across mythic, philosophical, physical, and Thalean grammars.

## Working frame

Public name:

    Structural Concordance

Technical name:

    B32K Concordance Ledger

Method:

    translation mythology
    declared correlation
    structural function extraction
    JSON artifact tracking first
    database later, when query pressure requires it

## Current seed

Genesis 1 is being read as a grammar of emergence:

- creation as boundary action
- light as first receipt
- heaven as first chamber
- earth as first field of embodied grammar
- seed as recursive memory
- lights as recurrence clock
- life as moving witness

## Data policy

Raw source text goes in:

    data/source/

Working extracts go in:

    data/working/

Machine-readable artifacts go in:

    artifacts/json/

Schemas go in:

    artifacts/schema/

Human notes go in:

    notes/

Reports go in:

    reports/

The filesystem is the first ledger.

## Indexing contract

The current repository distinguishes three coordinates:

- catalogue addresses are one-based, from 1 through 32768;
- wire indices are zero-based, from 0 through 32767;
- lane indices are zero-based and scoped to a named lane.

The exact conversion is:

    wire_index = catalogue_address - 1
    catalogue_address = wire_index + 1

Catalogue address 0 is outside the registry. Catalogue address 1 maps
to wire and lane index 0. In the Aletheos-bound lane this is the
registered `NULL_WELL` boundary and carries no positive authority.

Catalogue address 2 maps to wire/lane index 1, `B32K_BOOTLOADER`, and is reserved for B32K itself.

Organization space begins at catalogue address 3, wire/lane index 2. Ordinary allocatable positions begin at catalogue address 4, wire/lane index 3. Aletheos root language elsewhere in this repository is lane-bound and pre-ratification.
Catalogue address 32768 maps to the maximum fifteen-bit wire index,
32767.

The machine-readable contract is
`artifacts/json/b32k_indexing_profile_001.json`. The explanatory
profile is `docs/spec/b32k_indexing_profile_001.md`.


## Address Space Convention 001

Package `0.3.0` records the finite-entry-point convention: actual null is outside the registry; catalogue 1/index 0 is `NULL_WELL`; catalogue 2/index 1 is `B32K_BOOTLOADER`; catalogue 3/index 2 is `ORGANIZATION_ROOT`; catalogue 4..32768 are remaining typed entry points into lanes or contexts.

## Bootstrap Map 001

Package `0.4.0` defines the stable hierarchical bootstrap map:

    b32k.1          null indexer
    b32k.2          self-referencing B32K bootloader
    b32k.2.1        public B32K shell
    b32k.3          organization root
    b32k.3.1.1      organization bootloader
    b32k.3.1.2      organization API
    b32k.4          first ordinary lane

The B32K bootloader verifies and receipts a claimed B32K packet. Its sole external action is to pipe the packet unchanged from `b32k.2.1` to `b32k.3.1.1`.

The organization API at `b32k.3.1.2` remains separately authenticated and admitted. Public shell access and API discovery confer neither trust nor authority.

See `artifacts/json/b32k_bootstrap_map_001.json` and `docs/spec/b32k_bootstrap_map_001.md`.

## Orientation CLI

Package `0.5.0` provides the local B32K orientation CLI.

    b32k orient
    b32k resolve org.api
    b32k get b32k.2.1
    b32k mount rookos

Bootstrap Map 002 adds the permanent public organization label at `b32k.3.1`, the public cryptographic disclosure at `b32k.3.1.2`, and the organization API at `b32k.3.2.1`.

The local mount adapter invokes an installed `rookos.cli` entry point. Mounting does not authenticate a principal, grant authority, select a hat, or mutate RookOS by itself.
