#!/bin/zsh
set -eu
repo=${0:A:h}
control="$HOME/Library/Application Support/RClassroom-v1"
runtime="${R_CLASSROOM_RUNTIME:-$control}"
if [[ -z "${R_CLASSROOM_RUNTIME:-}" && -f "$control/runtime-path.txt" ]]; then
  runtime=$(cat "$control/runtime-path.txt")
fi
if [[ ! -x "$runtime/environment/bin/python" ]]; then
  /bin/zsh "$repo/setup-mac.command"
fi
exec "$runtime/bin/micromamba" --no-rc --root-prefix "$runtime/mamba-root" run --prefix "$runtime/environment" python "$repo/tools/classroom.py" --runtime "$runtime" --stop
