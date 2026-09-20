# Disk Stress Testing

Benchmarks storage subsystems with fio, dd, hdparm, and iostat to measure IOPS, throughput, and latency under load.

## Instructions

# Disk Stress Testing

## What this skill does

Disk stress testing quantifies how a storage subsystem behaves under sustained IO. fio generates controlled workloads (IOPS, throughput, latency), dd does quick raw writes, and iostat/hdparm give live device-level statistics.

## When to use

- Validating new VMs or bare-metal nodes before production cutover
- Comparing IO performance between storage classes (SSD, NVMe, network storage)
- Reproducing latency complaints from a busy database

## Real commands

```bash
# 4k random write IOPS test with O_DIRECT
fio --name=randwrite --ioengine=libaio --iodepth=16 --rw=randwrite \
  --bs=4k --size=4G --numjobs=1 --runtime=60 --time_based --direct=1

# 1M sequential read throughput
fio --name=seqread --ioengine=libaio --iodepth=32 --rw=read --bs=1M \
  --size=8G --runtime=60 --time_based --direct=1

# Quick raw write + flush
sudo dd if=/dev/zero of=/tmp/testfile bs=1M count=4096 oflag=direct conv=fdatasync

# Device-level cache/throughput
sudo hdparm -tT /dev/sda

# Live stats: tps, await, util%
iostat -x 2 5
```

## Interpreting fio output

Look for the `bw` (MiB/s), `iops`, and `clat` (percentile latencies) lines. For databases, p99 clat below 10 ms for 4k random IO is typical on NVMe; above 50 ms signals a problem.

## Testing checklist

```bash
# Run before and after any storage change for comparison
fio --name=bw --ioengine=libaio --direct=1 --rw=read --bs=1M --size=4G --numjobs=4 --runtime=30 --time_based
```

## Best practices

- Always use `--direct=1` to bypass the page cache and measure real device IO.
- Run each benchmark 3 times and take the median.
- Check `iostat -x` `%util` and `await` during the run, not just fio totals.
- Never benchmark a disk that hosts the OS while it is under production load.
- Clean up test files (`rm -f /tmp/testfile`) after dd runs.

## Capabilities

### io-benchmark
Run fio jobs, raw dd writes, and live IO statistics to characterize disk performance and detect degradation.

**Commands:**
- `fio --name=randwrite --ioengine=libaio --iodepth=16 --rw=randwrite --bs=4k --size=4G --numjobs=1 --runtime=60 --time_based --direct=1`
- `fio --name=seqread --ioengine=libaio --iodepth=32 --rw=read --bs=1M --size=8G --runtime=60 --time_based --direct=1`
- `dd if=/dev/zero of=/tmp/testfile bs=1M count=4096 oflag=direct conv=fdatasync`
- `hdparm -tT /dev/sda`
- `iostat -x 2 5`

**Examples:**
- fio --name=randread --ioengine=libaio --iodepth=16 --rw=randread --bs=4k --size=4G --runtime=60 --time_based --direct=1
- dd if=/dev/zero of=/tmp/testfile bs=1M count=4096 oflag=direct conv=fdatasync && rm -f /tmp/testfile
- iostat -x 2 5 | grep sda