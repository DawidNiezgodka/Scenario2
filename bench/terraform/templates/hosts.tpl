%{ for cfg in configuration ~}
%{ for role in cfg.labels.role ~}
[${role}]
%{ for vm in vm_info ~}
%{ if substr(vm.name, 0, length(cfg.name)) == cfg.name ~}
%{ if role == "zookeeper-nodes" ~}
${vm.name} ansible_host=${vm.ext_ip} zookeeper_id=${vm.index}
%{ else ~}
${vm.name} ansible_host=${vm.ext_ip}
%{ endif ~}
%{ endif ~}
%{ endfor ~}
%{ endfor ~}
%{ endfor ~}
