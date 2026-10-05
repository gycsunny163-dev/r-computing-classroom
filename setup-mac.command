#!/bin/zsh
set -eu
trap 'echo "Setup failed. Keep the error text for diagnosis."; [[ -t 0 ]] && read "?Press Return to close."; exit 1' ERR
repo=${0:A:h}
control="$HOME/Library/Application Support/RClassroom-v1"
runtime="${R_CLASSROOM_RUNTIME:-$control}"
if [[ -z "${R_CLASSROOM_RUNTIME:-}" && -f "$control/runtime-path.txt" ]]; then
  runtime=$(cat "$control/runtime-path.txt")
fi
mkdir -p "$runtime/bin"
case "$(uname -m)" in
  arm64) target=osx-arm64 ;;
  x86_64) target=osx-64 ;;
  *) echo 'This Mac architecture is not supported.'; exit 1 ;;
esac
if [[ ! -x "$runtime/bin/micromamba" ]]; then
  curl --fail --location --silent --show-error "https://micro.mamba.pm/api/micromamba/$target/latest" -o "$runtime/micromamba.tar.bz2"
  tar -xjf "$runtime/micromamba.tar.bz2" -C "$runtime" bin/micromamba
fi
if [[ ! -x "$runtime/environment/bin/python" ]]; then
  "$runtime/bin/micromamba" create --yes --no-rc --root-prefix "$runtime/mamba-root" --prefix "$runtime/environment" --file "$repo/environment.yml"
fi
"$runtime/bin/micromamba" --no-rc --root-prefix "$runtime/mamba-root" run --prefix "$runtime/environment" python "$repo/tools/setup_local.py" --runtime "$runtime"
mkdir -p "$control"
printf '%s' "$runtime" > "$control/runtime-path.txt"
echo 'Ready. Open start-mac.command when you want to enter the classroom.'
