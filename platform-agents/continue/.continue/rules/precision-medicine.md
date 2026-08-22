---
name: "precision-medicine"
description: "Analyzes genomic and clinical data with bioinformatics tooling: alignment QC with samtools, variant filtering with bcftools, and BLAST searches."
globs: ["**/*.r", "**/*.sh"]
alwaysApply: false
---

# precision-medicine

Analyzes genomic and clinical data with bioinformatics tooling: alignment QC with samtools, variant filtering with bcftools, and BLAST searches.

## Instructions

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