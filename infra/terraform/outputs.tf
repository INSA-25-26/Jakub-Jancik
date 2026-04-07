output "instance_public_ip" {
  description = "Public IP of the deployed VM."
  value       = aws_instance.app_vm.public_ip
}

output "instance_dns" {
  description = "Public DNS of the deployed VM."
  value       = aws_instance.app_vm.public_dns
}

output "ecr_repository_url" {
  description = "ECR repository URL for docker push/pull."
  value       = aws_ecr_repository.app_repo.repository_url
}
