variable "vault_password" {
  default = ".vault/brukshut-vault-password"
  type = string
}

locals {
  ansible_args = ["-b", "--vault-password-file=${var.vault_password}", "-vv"]
}

source "docker" "dovecot" {
  image = "debian:latest"
  commit = true
  changes = [
    "USER dovecot",
    "WORKDIR /usr/local/share/dovecot",
    "ENV HOSTNAME mail.gturn.xyz",
    "VOLUME /export/home",
    "EXPOSE 993",
    "LABEL version=2.3.17",
    "CMD [\"/usr/local/sbin/dovecot\", \"-F\"]"
  ]
}

build {
  sources = ["source.docker.dovecot"]

  provisioner "shell" {
    script = "scripts/install_packages.sh"
  }

  provisioner "ansible" {
    playbook_file   = "playbooks/dovecot.yml"
    extra_arguments = local.ansible_args
  }
}
