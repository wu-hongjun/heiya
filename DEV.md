# Developer Commands

> **Stuff in this document is developer information and is irrelevent to normal users.**

## Commands for Twine

### CD to Repository
`cd /Users/hongjunwu/Documents/GitHub/heiya`

### Build Package
`python3 setup.py sdist bdist_wheel`

### Upload Package
`python3 -m twine upload dist/*`

### Delete Distributed Binaries
`rm -r ./dist`
