provider "google" {
  project = ""
  region = ""
  zone = ""
}

variable "server_port" {
  description = "the port the server will use for http reqs"
  type = number
  default = 8081
}

output "external_ip" {
  value = google_compute_instance.example.network_interface.0.access_config.0.nat_ip
}

resource "google_compute_network" "mynetwork" {
  name = "mynetwork"
  auto_create_subnetworks = true
}

resource "google_compute_instance" "example" {
  name = "my-vm1"
  machine_type = "n2-standard-2"
  tags = ["edge-server"]
  zone = "europe-west1-b"


  boot_disk {
    initialize_params {
      image = "ubuntu-2004-focal-v20221213"
    }
  }

  network_interface {
    network = google_compute_network.mynetwork.self_link
    access_config {
      nat_ip = google_compute_address.static.address
    }
  }

  metadata = {
    startup-script = <<-EOF
        #!/bin/bash
        sudo snap install docker
        sudo docker version > file1.txt
        sleep 5
        sudo docker run -d --rm -p ${var.server_port}:${var.server_port} \
        busybox sh -c "while true; do { echo -e 'HTTP/1.1 200 OK\r\n'; \
        echo 'yo'; } | nc -l -p ${var.server_port}; done"
        EOF
  }

}

resource "google_compute_address" "static" {
  name = "ipv4-address"
}






