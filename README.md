# README

## Introduction

This is a collection of quick and simple tools/scripts that might assist in during DFIR. The tools themselves should not be seen as preserving evidence, you should take copies of the original files or an image of a machine if you need that. 

The tools are primarily to make responding quicker. 

## Tools

### macOS

#### browser_history.py

This script takes a single command line argument as a valid user, or runs as the current user. 
It dumps the browser history for the three main browsers into the `/tmp/` directory as CSVs, ideal for picking up using an RMM or similar. 
**Usage**
`browser_history.py username`
