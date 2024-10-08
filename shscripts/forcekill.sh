#!/bin/bash

pids=$(ps aux | grep '[P]ython' | awk '{print $2}')
# kill -9 $pids
kill $pids