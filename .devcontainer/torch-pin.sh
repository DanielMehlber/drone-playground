#!/usr/bin/env bash
# shellcheck disable=SC2034
# Shared pin for the dev container scripts. The two ends of the MPS bridge
# refuse each other unless this PyTorch version is the same on both.
# docker/Dockerfile repeats TORCH_VERSION; keep the two in step.

export TORCH_VERSION=2.15.0
export TORCH_CPU_INDEX=https://download.pytorch.org/whl/cpu
export TORCH_CUDA_INDEX=https://download.pytorch.org/whl/cu128
export VARCO_COMMIT=1bdc616915433fcbc2d6b2748fa95319f11fffce
export VARCO_URL=https://github.com/FabioMalpezzi/varco.git
export VARCO_PORT=47700
