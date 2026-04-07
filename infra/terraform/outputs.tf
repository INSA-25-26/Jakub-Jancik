output "instance_public_ip" {
  description = "Public IP of the deployed VM."
  value       = aws_instance.app_vm.public_ip
}

output "instance_dns" {
  description = "Public DNS of the deployed VM."
  value       = aws_instance.app_vm.public_dns
}
