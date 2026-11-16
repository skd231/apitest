def lambda_handler(event, context):
  a = int(event.get("a", 0))
  b = int(event.get("b", 0))

  is_negative = (a < 0) ^ (b < 0)
  num = abs(a)
  times = abs(b)

  if num < times:
    num, times = times, num

  total = 0
  for _ in range(times):
    total += num

  if is_negative and total != 0:
    total = -total

  return {"result": total, "iterations": times}
