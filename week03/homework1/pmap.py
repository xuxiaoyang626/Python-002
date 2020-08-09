import argparse
import ipaddress
import os
import json
from multiprocessing import Manager
from multiprocessing.pool import Pool

def ping(hostname):
  print(hostname)
  response = os.system("ping -c 1 " + hostname)

  if response == 0:
    print(f'{hostname}, "is up!"')
  else:
    print(f'{hostname}, "is down!"')
  return hostname

def parse_ip_range(ip_string):
  ips = ip_string.split("-")
  # single ip
  if len(ips) == 1:
    return ipaddress.IPv4Address(ips[0]), ipaddress.IPv4Address(ips[0])
  # ip range
  elif len(ips) == 2:
    start_ip = ipaddress.IPv4Address(ips[0])
    end_ip = ipaddress.IPv4Address(ips[1])
    if start_ip > end_ip:
      raise Exception(f'ip range {ip_string} is incorrect, start ip should be smaller than end ip')
    return start_ip, end_ip
  # invalid ip range
  else:
    raise Exception("invalid ip range, please follow format x.x.x.x-x.x.x.x")

def save_as_json(filepath, content):
  with open(filepath, 'w') as f:
    f.write(content)

if __name__ == "__main__":
  # parse command line options
  parser = argparse.ArgumentParser(description="scan available ip range or ports")
  parser.add_argument("-n", "--numOfParallel", type=int, help="number of parallel jobs")
  parser.add_argument("-f", "--functionOfScan", type=str, choices=["tcp", "ip"], help="function of to use for scanning", required=True)
  parser.add_argument("-ip", "--ipRange", type=str, help="ip address or an ip range", required=True)
  parser.add_argument("-w", "--writeToFile", type=str, help="file name to write output to")
  args = parser.parse_args()

  parallel = args.numOfParallel
  mode = args.functionOfScan
  ip_string = args.ipRange
  filename = args.writeToFile

  # validate output file name
  if filename:
    if not filename.endswith(".json"):
      raise ValueError("output file has to be json")
  
  # configure process pool size
  p = Pool()
  if parallel:
    p = Pool(parallel)

  # parse ip range
  start_ip, end_ip = "", ""
  try: 
    start_ip, end_ip = parse_ip_range(ip_string)
    print(f'Start IP: {start_ip}')
    print(f'End IP: {end_ip}')
  except Exception as e:
    print("invalid ip string\n", e)
    exit(1)

  # main scan logic
  print("Start scanning...")
  output_list = []
  for ip_int in range(int(start_ip), int(end_ip)):
    res = p.apply_async(ping, args=(str(ipaddress.IPv4Address(ip_int)),))
    print(type(res.get(timeout=30)))

  p.close()
  p.join()
  print("Scan finished.")
  p.terminate()

  # write to output file
  #if filename:
  #  while not q.empty():
  #    output_list.append(q.get())
  #    save_as_json(filename, json.dumps(output_list))



