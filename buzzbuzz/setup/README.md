# Instructions

This challenge requires a bit more setup.

1. Spin up a GCE VM and copy webserv in. Install the `requirements.txt` and run `main.py`.
2. Clone Samuel Colvin's [dnserver](https://github.com/samuelcolvin/dnserver/). Replace the `dnserver/dnserver/main.py` file with that found in the dnserv directory and place `run.py` in `dnserver/`. Replace the `example_zones.toml` with the file in dnserv, and fill in the bottommost entry with your host. Run `run.py`.
3. Make sure that dns and http-alt are enabled and permitted by any firewall rules.
4. Add a DNS A record for `aeyie4lei1aidie7.in-scope` pointing to the GCE VM's IP.
5. Add a DNS NS record for `d25d-44ff-b3aa-1bd573335cbf.aeyie4lei1aidie7.in-scope` pointing to the FQDN of the GCE VM.

Note that our domain was `irisc.tf` for IrisCTF 2024. If you're running this in the future for a lab or something, you may need to do some modifications for your own use case.

When in doubt, you can contact@irisc.tf.

Good luck! -skat
