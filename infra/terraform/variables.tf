variable "aws_region" {
  description = "AWS region for infrastructure."
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Project name prefix."
  type        = string
  default     = "telco-churn"
}

variable "instance_type" {
  description = "EC2 instance size."
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Existing AWS key pair name for SSH."
  type        = string
}

variable "allowed_ssh_cidr" {
  description = "CIDR allowed to SSH to instance."
  type        = string
  default     = "0.0.0.0/0"
}

variable "ecr_repository_name" {
  description = "ECR repository name for application image."
  type        = string
  default     = "telco-churn"
}
