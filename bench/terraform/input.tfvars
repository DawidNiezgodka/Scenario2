project = "project"
service_account_email = "sa@project.iam.gserviceaccount.com"
gcp_user = "user"
world_reachable_protocol_port_map = {
  tcp = "22,80,8080,5683,8000,9000"
}
configuration = [
{
  name = "edge-server"
  count = 1
  tags = [
  "edge-server"
]
  labels = {
  role = [
  "edge-servers"
]
}
  machine_type = "n2-standard-2"
  image = "ubuntu-2004-focal-v20231023"
},
{
  name = "wg"
  count = 1
  tags = [
  "wg"
]
  labels = {
  role = [
  "workload-generators"
]
}
  machine_type = "n2d-standard-4"
  image = "ubuntu-2004-focal-v20231023"
}
]
