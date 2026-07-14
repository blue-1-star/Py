<!-- Added 2026-07-04 20:57:54 -->

# OSBB Development Conventions

## Working Directory

Unless explicitly required otherwise, all development work is performed from the project root:

`G:\Programming\Py\OSBB`

This includes:

- git commands
- Python tools
- maintenance scripts
- generators
- Runner utilities
- documentation writers

Tools should use project-relative paths whenever possible.

## Safe Change Process

Default sequence:

1. Inspect current state.
2. Run dry-run.
3. Create backup if data or source files will change.
4. Apply.
5. Run validation:
   - `python -m py_compile ...`
   - targeted smoke test
6. Commit meaningful stage to Git.
7. Update documentation.

## Project Documentator

The Project Documentator is a standing project role.

No architectural decision is considered complete until the relevant documentation is updated.

Documentation targets:

- `MODULE.md`
- component `*.MODULE.md`
- `README.md`
- `KNOWLEDGE/*.md`
- migration reports in `Recovered/`

The Documentator tracks:

- why a decision was made
- where the implementation lives
- how to test it
- how to roll it back
- what still remains planned
