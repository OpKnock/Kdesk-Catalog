---
type: agent_requested
description: "Analyzes genomic and clinical data with bioinformatics tooling: alignment QC with samtools, variant filtering with bcftools, and BLAST searches. Use when working with alignment, variants or when the user mentions alignment, variants."
---

Analyzes genomic and clinical data with bioinformatics tooling: alignment QC with samtools, variant filtering with bcftools, and BLAST searches.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `samtools flagstat sample.bam`, `bcftools stats variants.vcf.gz > stats.txt`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

# Precision Medicine

Process genomic data reproducibly with the htslib toolchain.

## When to Use

- Variant calling QC and filtering
- Aligning or assessing WGS/WES reads
- Cohort comparison on variant burden

## Alignment QC

```bash
samtools flagstat sample.bam
samtools idxstats sample.bam
```

Check: total reads, mapped %, duplicates, and per-chromosome coverage.

## Region extraction

```bash
samtools index sample.bam
samtools view -b -o chr1.bam sample.bam chr1
```

## Variant QC

```bash
bcftools stats variants.vcf.gz > stats.txt
bcftools view -i 'QUAL>30 && DP>20' variants.vcf.gz | bcftools query -f '%CHROM\t%POS\t%REF\t%ALT\n' | head
```

## Filtering policy

- Genotype quality and depth thresholds per platform.
- Keep PASS-only calls in clinical pipelines.
- Annotate with VEP/ANNOVAR before interpretation.

## Best practices

- Record pipeline versions with every dataset.
- Use gzip+bcsf compressed VCFs for storage.
- Never round-trip BAM through text without flags preservation.
- Validate sample IDs against manifests early.

## Testing

Run flagstat/stats on a control sample and compare against the reference baseline.

## Capabilities

### alignment
Inspect and QC aligned sequencing data.

**Parameters:**
- `bam` (string): Alignment file
- `region` (string): chr:start-end region
- `filter` (string): SAM flag filter like -F 4

**Commands:**
- `samtools flagstat sample.bam`
- `samtools view -h sample.bam | head -30`
- `samtools view -b -o chr1.bam sample.bam chr1`
- `samtools idxstats sample.bam`
- `samtools depth -a -r chr1:1000-2000 sample.bam | head`

**Examples:**
- samtools flagstat sample.bam | grep -E 'total|mapped'
- samtools view -c -F 4 sample.bam
- samtools index sample.bam && samtools idxstats sample.bam | head -10

### variants
Filter and summarize variant calls.

**Parameters:**
- `vcf` (string): Variant call file
- `expression` (string): bcftools filter expression
- `format` (string): bcftools query output format

**Commands:**
- `bcftools stats variants.vcf.gz > stats.txt`
- `bcftools view -f PASS variants.vcf.gz`
- `bcftools view -i 'QUAL>30 && DP>20' variants.vcf.gz | bcftools query -f '%CHROM\t%POS\t%REF\t%ALT\n' | head`
- `bcftools filter -i 'INFO/DP>20' -o filtered.vcf.gz variants.vcf.gz`
- `bcftools query -l variants.vcf.gz`

**Examples:**
- bcftools view -i 'INFO/AF>0.1' variants.vcf.gz | bcftools stats - | head -40
- bcftools query -f '%CHROM:%POS %REF>%ALT %QUAL\n' variants.vcf.gz | head
- bcftools view -v snps variants.vcf.gz | bcftools stats - > snps.stats

## References
- [samtools](https://www.htslib.org/doc/samtools.html)
- [bcftools](https://samtools.github.io/bcftools/)
- [NCBI BLAST](https://www.ncbi.nlm.nih.gov/books/NBK279690/)