
# Christmas Broadcasts Collection Guide

## Overview
Queen Elizabeth II delivered annual Christmas broadcasts from 1952 to 2021.
These speeches provide consistent year-over-year content and are often available
in the public domain or through official royal archives.

## Collection Strategy

### Priority Years (Represent different eras):
1. 1952 - First Christmas broadcast (early reign)
2. 1957 - First televised broadcast
3. 1977 - Silver Jubilee year
4. 1991 - Gulf War period
5. 1997 - Death of Princess Diana
6. 2002 - Golden Jubilee year
7. 2012 - Diamond Jubilee year
8. 2020 - COVID-19 pandemic
9. 2021 - Final Christmas broadcast

### Sources:
- Royal.uk official transcripts (limited availability)
- British Library archives
- National Archives (UK)
- Academic databases and historical collections

## Data Entry Format:

```python
speech = {
    "title": "Christmas Broadcast 1952",
    "date": "1952-12-25",
    "category": "christmas_broadcast",
    "occasion": "First Christmas Broadcast as Queen",
    "location": "Sandringham House",
    "content": "[Full speech text here]",
    "source": {
        "url": "https://...",
        "description": "Official royal archives"
    },
    "notes": "First broadcast after accession to throne in February 1952"
}
```

## Token Estimation:
- Average Christmas broadcast: 600-1000 words (~460-770 tokens)
- 70 broadcasts total (1952-2021): ~35,000-50,000 tokens potential
- Priority: Collect at least 10 representative broadcasts (~5,000-7,000 tokens)
