output "segment_id" {
  description = "Stable identifier allocated for this segment."
  value       = random_id.segment.hex
}

output "listen_port" {
  description = "Port echoed back from input, as a real module would."
  value       = var.port
}

# Returned as a list (one policy ID per domain, ordered to match var.domains).
# The terraform-module schema inference maps list(string) cleanly to a typed
# Sequence[str] in the generated SDK; a map(string) output would be inferred as
# a sequence and fail output translation at runtime.
output "domain_policy_ids" {
  description = "Allocated policy IDs, one per domain (same order as input)."
  value       = [for d in var.domains : random_id.policy[d].hex]
}

output "domain_count" {
  description = "Number of domains in this segment."
  value       = length(var.domains)
}
