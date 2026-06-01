# SkillNet Frontend Snapshot

This folder contains a local snapshot of the SkillNet Streamlit frontend pulled from the overseas server.

## Source

- Server path: `/opt/SKillNet_Dev/skillnet-web-new`
- Runtime venv on server: `/opt/SKillNet_Dev/skillnet_frontend`
- Current server command:

```bash
cd /opt/SKillNet_Dev/skillnet-web-new
/opt/SKillNet_Dev/skillnet_frontend/bin/streamlit run app_new.py --server.port 80 --server.address 0.0.0.0
```

## Local Layout

- `skillnet-web-new/`: Streamlit app source
- `sync_stats.py`: stats synchronization script from the server
- `skillnet-web-new-source.tar.gz`: original source archive copied from the server

The server virtual environment was not copied. Runtime/cache folders and `.streamlit/secrets.toml` were excluded.

## Local Environment

The local Streamlit development environment should live in the shared workspace environment
directory:

```bash
cd /home/jiangchen/Skill_Fabric
python3 -m venv environment/SkillNet_dev
environment/SkillNet_dev/bin/python -m pip install -r SkillNet/requirements-dev.txt
```

Run the frontend locally:

```bash
cd /home/jiangchen/Skill_Fabric/SkillNet/skillnet-web-new
/home/jiangchen/Skill_Fabric/environment/SkillNet_dev/bin/streamlit run app_new.py
```

## Secrets

The frontend reads Supabase config from Streamlit secrets:

```toml
[supabase]
SUPABASE_URL = "..."
SUPABASE_KEY = "..."
```

Only anon/public keys should be used by the frontend. Service role keys must remain server-side.
