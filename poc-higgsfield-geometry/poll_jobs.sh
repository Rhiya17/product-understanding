#!/bin/bash
# Poll Higgsfield jobs until terminal state; download completed videos to out/.
# usage: ./poll_jobs.sh <name:request_id> [<name:request_id> ...]
# (bash 3.2 compatible — uses marker files instead of associative arrays)
cd "$(dirname "$0")" && source .env
mkdir -p out
while :; do
  all_done=1
  for job in "$@"; do
    name="${job%%:*}"; id="${job#*:}"
    [ -f "out/.done_$name" ] && continue
    resp=$(curl -s "https://platform.higgsfield.ai/requests/$id/status" \
      -H "hf-api-key: $HIGGSFIELD_API_KEY" -H "hf-secret: $HIGGSFIELD_API_SECRET")
    status=$(echo "$resp" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("status","?"))')
    echo "$(date +%H:%M:%S) $name: $status"
    case "$status" in
      completed)
        url=$(echo "$resp" | python3 -c 'import json,sys; d=json.load(sys.stdin); print((d.get("video") or {}).get("url",""))')
        if [ -n "$url" ]; then curl -s -o "out/$name.mp4" "$url" && echo "$name saved -> out/$name.mp4"; fi
        echo "$resp" > "out/$name.result.json"; touch "out/.done_$name" ;;
      failed|nsfw)
        echo "$resp" > "out/$name.result.json"; touch "out/.done_$name" ;;
      *) all_done=0 ;;
    esac
  done
  [ "$all_done" = 1 ] && break
  sleep 20
done
echo "all jobs terminal"
