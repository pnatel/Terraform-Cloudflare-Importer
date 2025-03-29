terraform {
    required_providers {
        cloudflare = {
            source = "cloudflare/cloudflare"
            version = "~> 5"
        }	
    }
}

variable "API_TOKEN" {}

provider "cloudflare" {
    api_token  = var.API_TOKEN
}