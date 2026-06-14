resource "random_string" "unique_suffix" {
   length  = 8
   special = false
   upper   = false
}