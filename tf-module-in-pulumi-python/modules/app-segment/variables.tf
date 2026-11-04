variable "name" {
  description = "Logical name of the application segment."
  type        = string
}

variable "domains" {
  description = "FQDNs that belong to this segment."
  type        = list(string)
}

variable "port" {
  description = "TCP port the segment listens on."
  type        = number
  default     = 443
}
