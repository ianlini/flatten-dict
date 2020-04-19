#!/bin/bash
set -ex

rm -rf dist
poetry build
