podman kill $(podman ps -q) || true
podman rm $(podman ps -aq) || true