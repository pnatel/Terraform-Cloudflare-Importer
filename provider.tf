terraform {
    required_providers {
        cloudflare = {
            source = "cloudflare/cloudflare"
        }	
    }
}

variable "API_TOKEN" {}

provider "cloudflare" {
    api_token  = var.API_TOKEN
}