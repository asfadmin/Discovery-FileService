# Discovery-FileService

Simple service to generate and serve random file data for testing purposes.

## Usage

There is one single endpoint available:

`/generate` _(GET, POST)_
- Parameters:
    - `bytes` _(Optional)_ File size in bytes. Rounds up to next 1000. Default is "1000", max is 1e10 (10GB)
    - `slow` _(Optional)_ Microseconds to delay between 1000-byte chunks when sending data. Default is "0"

## Examples

_Default 1KB file generated at full speed:_
- https://filegen-dev.asf.alaska.edu/generate
  
_Generate a 10KB file at full speed:_
- https://filegen-dev.asf.alaska.edu/generate?bytes=10000
  
_Generate a 1MB file with a 400us slowdown between 1KB chunks:_
- https://filegen-dev.asf.alaska.edu/generate?bytes=1000000&slow=400