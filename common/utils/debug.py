def dump_var(var, name="var"):
   print(f"Name: {name}")
   print(f"Type: {type(var)}")
   print(f"Value: {repr(var)}")

   if isinstance(var, (int, bytes)):
      print(f"Hex: {hex(var) if isinstance(var, int) else var.hex()}")

   print(f"Dir: {dir(var)}")

   if hasattr(var, '__dict__'):
      print(f"Attributes: {vars(var)}")

if __name__ == "__main__":
   dump_var("yourmom")