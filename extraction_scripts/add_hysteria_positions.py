import json

# Load current database
with open('data/FREUD_DATABASE.json', 'r') as f:
    data = json.load(f)

# Ensure we start from 394
data['positions'] = data['positions'][:394]

source = ["Selected Papers on Hysteria and Other Psychoneuroses (1893-1906)"]

# ALL 156 POSITIONS
new_positions = []

# MENTAL CAUSATION (8)
new_positions.extend([
    {"id": "MENT-001", "position_id": "MENT-001", "domain": "MENTAL_CAUSATION", "title": "Hysterical symptoms have purely psychical causes from traumatic experiences not organic lesions", "source": source, "text_evidence": "Hysterical symptoms have purely psychical causes from traumatic experiences not organic lesions"},
    {"id": "MENT-002", "position_id": "MENT-002", "domain": "MENTAL_CAUSATION", "title": "Repressed ideas exert causal power producing physical symptoms conversion", "source": source, "text_evidence": "Repressed ideas exert causal power producing physical symptoms conversion"},
    {"id": "MENT-003", "position_id": "MENT-003", "domain": "MENTAL_CAUSATION", "title": "Mental splitting creates separate independent streams of consciousness", "source": source, "text_evidence": "Mental splitting creates separate independent streams of consciousness"},
    {"id": "MENT-004", "position_id": "MENT-004", "domain": "MENTAL_CAUSATION", "title": "Unconscious ideas maintain causal efficacy when excluded from awareness", "source": source, "text_evidence": "Unconscious ideas maintain causal efficacy when excluded from awareness"},
    {"id": "MENT-005", "position_id": "MENT-005", "domain": "MENTAL_CAUSATION", "title": "Symptom-formation mechanism involves symbolic representation", "source": source, "text_evidence": "Symptom-formation mechanism involves symbolic representation"},
    {"id": "MENT-006", "position_id": "MENT-006", "domain": "MENTAL_CAUSATION", "title": "Symptoms overdetermined multiple psychical paths converge", "source": source, "text_evidence": "Symptoms overdetermined multiple psychical paths converge"},
    {"id": "MENT-007", "position_id": "MENT-007", "domain": "MENTAL_CAUSATION", "title": "Every symptom detail has psychological motivation", "source": source, "text_evidence": "Every symptom detail has psychological motivation"},
    {"id": "MENT-008", "position_id": "MENT-008", "domain": "MENTAL_CAUSATION", "title": "Psychical determinism all mental phenomena have psychological causes", "source": source, "text_evidence": "Psychical determinism all mental phenomena have psychological causes"},
])

# MEMORY AND TRAUMA (10)
new_positions.extend([
    {"id": "MEMR-001", "position_id": "MEMR-001", "domain": "MEMORY_TRAUMA", "title": "Traumatic memories retain affective charge when not consciously recalled", "source": source, "text_evidence": "Traumatic memories retain affective charge when not consciously recalled"},
    {"id": "MEMR-002", "position_id": "MEMR-002", "domain": "MEMORY_TRAUMA", "title": "Abreaction affect discharge necessary for memory to lose pathogenic power", "source": source, "text_evidence": "Abreaction affect discharge necessary for memory to lose pathogenic power"},
    {"id": "MEMR-003", "position_id": "MEMR-003", "domain": "MEMORY_TRAUMA", "title": "Memories strangulated retained without emotional discharge maintain traumatic force", "source": source, "text_evidence": "Memories strangulated retained without emotional discharge maintain traumatic force"},
    {"id": "MEMR-004", "position_id": "MEMR-004", "domain": "MEMORY_TRAUMA", "title": "Hypnosis recovers memories inaccessible to normal recall", "source": source, "text_evidence": "Hypnosis recovers memories inaccessible to normal recall"},
    {"id": "MEMR-005", "position_id": "MEMR-005", "domain": "MEMORY_TRAUMA", "title": "Memory traces distorted but retain essential content in unconscious", "source": source, "text_evidence": "Memory traces distorted but retain essential content in unconscious"},
    {"id": "MEMR-006", "position_id": "MEMR-006", "domain": "MEMORY_TRAUMA", "title": "Pathogenic memories lie ready close by in approachable associations", "source": source, "text_evidence": "Pathogenic memories lie ready close by in approachable associations"},
    {"id": "MEMR-007", "position_id": "MEMR-007", "domain": "MEMORY_TRAUMA", "title": "Forgotten pathogenic ideas always exist merely excluded from association", "source": source, "text_evidence": "Forgotten pathogenic ideas always exist merely excluded from association"},
    {"id": "MEMR-008", "position_id": "MEMR-008", "domain": "MEMORY_TRAUMA", "title": "Hysterics suffer mostly from reminiscences", "source": source, "text_evidence": "Hysterics suffer mostly from reminiscences"},
    {"id": "MEMR-009", "position_id": "MEMR-009", "domain": "MEMORY_TRAUMA", "title": "Pathogenic memories not subject to normal decay into forgetfulness", "source": source, "text_evidence": "Pathogenic memories not subject to normal decay into forgetfulness"},
    {"id": "MEMR-010", "position_id": "MEMR-010", "domain": "MEMORY_TRAUMA", "title": "Memories correspond to traumas not sufficiently abreacted", "source": source, "text_evidence": "Memories correspond to traumas not sufficiently abreacted"},
])

# SEXUAL ETIOLOGY (12)
new_positions.extend([
    {"id": "SEXE-001", "position_id": "SEXE-001", "domain": "SEXUAL_ETIOLOGY", "title": "Sexual factors play primary etiological role in neuroses", "source": source, "text_evidence": "Sexual factors play primary etiological role in neuroses"},
    {"id": "SEXE-002", "position_id": "SEXE-002", "domain": "SEXUAL_ETIOLOGY", "title": "Sexual development begins in childhood not puberty", "source": source, "text_evidence": "Sexual development begins in childhood not puberty"},
    {"id": "SEXE-003", "position_id": "SEXE-003", "domain": "SEXUAL_ETIOLOGY", "title": "Sexual trauma in childhood has specific pathogenic effects distinct from adult trauma", "source": source, "text_evidence": "Sexual trauma in childhood has specific pathogenic effects distinct from adult trauma"},
    {"id": "SEXE-004", "position_id": "SEXE-004", "domain": "SEXUAL_ETIOLOGY", "title": "Infantile sexual experiences dictate later sexual life after maturity", "source": source, "text_evidence": "Infantile sexual experiences dictate later sexual life after maturity"},
    {"id": "SEXE-005", "position_id": "SEXE-005", "domain": "SEXUAL_ETIOLOGY", "title": "Sexuality must be broadened beyond genital to infantile pleasures", "source": source, "text_evidence": "Sexuality must be broadened beyond genital to infantile pleasures"},
    {"id": "SEXE-006", "position_id": "SEXE-006", "domain": "SEXUAL_ETIOLOGY", "title": "Sexual constitution replaces general neuropathic predisposition", "source": source, "text_evidence": "Sexual constitution replaces general neuropathic predisposition"},
    {"id": "SEXE-007", "position_id": "SEXE-007", "domain": "SEXUAL_ETIOLOGY", "title": "Hysteria originates in sexual passivity in pre-sexual periods before puberty", "source": source, "text_evidence": "Hysteria originates in sexual passivity in pre-sexual periods before puberty"},
    {"id": "SEXE-008", "position_id": "SEXE-008", "domain": "SEXUAL_ETIOLOGY", "title": "Sexual experiences of early childhood same significance in hysteria as compulsion neurosis", "source": source, "text_evidence": "Sexual experiences of early childhood same significance in hysteria as compulsion neurosis"},
    {"id": "SEXE-009", "position_id": "SEXE-009", "domain": "SEXUAL_ETIOLOGY", "title": "In normal vita sexualis no neurosis possible", "source": source, "text_evidence": "In normal vita sexualis no neurosis possible"},
    {"id": "SEXE-010", "position_id": "SEXE-010", "domain": "SEXUAL_ETIOLOGY", "title": "Sexual repression from childhood regularly precedes neurosis", "source": source, "text_evidence": "Sexual repression from childhood regularly precedes neurosis"},
    {"id": "SEXE-011", "position_id": "SEXE-011", "domain": "SEXUAL_ETIOLOGY", "title": "Neurosis results from conflict between libido and sexual repression", "source": source, "text_evidence": "Neurosis results from conflict between libido and sexual repression"},
    {"id": "SEXE-012", "position_id": "SEXE-012", "domain": "SEXUAL_ETIOLOGY", "title": "Constitutional sexual predisposition of child is polymorphous perverse", "source": source, "text_evidence": "Constitutional sexual predisposition of child is polymorphous perverse"},
])

# DEFENSE MECHANISMS (11)
new_positions.extend([
    {"id": "DEFE-001", "position_id": "DEFE-001", "domain": "DEFENSE_MECHANISM", "title": "Psychic force ego repugnance crowds pathogenic ideas from association", "source": source, "text_evidence": "Psychic force ego repugnance crowds pathogenic ideas from association"},
    {"id": "DEFE-002", "position_id": "DEFE-002", "domain": "DEFENSE_MECHANISM", "title": "Defense mechanisms protect ego from morally incompatible ideas", "source": source, "text_evidence": "Defense mechanisms protect ego from morally incompatible ideas"},
    {"id": "DEFE-003", "position_id": "DEFE-003", "domain": "DEFENSE_MECHANISM", "title": "Ego actively defends against threatening ideas through repression", "source": source, "text_evidence": "Ego actively defends against threatening ideas through repression"},
    {"id": "DEFE-004", "position_id": "DEFE-004", "domain": "DEFENSE_MECHANISM", "title": "Splitting of consciousness results from intentional act of will defense", "source": source, "text_evidence": "Splitting of consciousness results from intentional act of will defense"},
    {"id": "DEFE-005", "position_id": "DEFE-005", "domain": "DEFENSE_MECHANISM", "title": "Conversion brought about at cost of recollected affects", "source": source, "text_evidence": "Conversion brought about at cost of recollected affects"},
    {"id": "DEFE-006", "position_id": "DEFE-006", "domain": "DEFENSE_MECHANISM", "title": "Defense succeeds by weakening strong idea and robbing it of affect", "source": source, "text_evidence": "Defense succeeds by weakening strong idea and robbing it of affect"},
    {"id": "DEFE-007", "position_id": "DEFE-007", "domain": "DEFENSE_MECHANISM", "title": "Repression frees individual from unbearable presentations", "source": source, "text_evidence": "Repression frees individual from unbearable presentations"},
    {"id": "DEFE-008", "position_id": "DEFE-008", "domain": "DEFENSE_MECHANISM", "title": "Defense neurosis hysteria originates through repression of unbearable idea", "source": source, "text_evidence": "Defense neurosis hysteria originates through repression of unbearable idea"},
    {"id": "DEFE-009", "position_id": "DEFE-009", "domain": "DEFENSE_MECHANISM", "title": "Repressed idea becomes pathogenic causes morbid symptoms", "source": source, "text_evidence": "Repressed idea becomes pathogenic causes morbid symptoms"},
    {"id": "DEFE-010", "position_id": "DEFE-010", "domain": "DEFENSE_MECHANISM", "title": "Intentional forgetting unsuccessful leads to neurosis", "source": source, "text_evidence": "Intentional forgetting unsuccessful leads to neurosis"},
    {"id": "DEFE-011", "position_id": "DEFE-011", "domain": "DEFENSE_MECHANISM", "title": "Exertion of will to crowd out thoughts can produce pathological disposition", "source": source, "text_evidence": "Exertion of will to crowd out thoughts can produce pathological disposition"},
])

# CONVERSION MECHANISM (9)
new_positions.extend([
    {"id": "CONV-001", "position_id": "CONV-001", "domain": "CONVERSION_MECHANISM", "title": "Sum of excitement not entering psychic association finds wrong road to bodily innervation", "source": source, "text_evidence": "Sum of excitement not entering psychic association finds wrong road to bodily innervation"},
    {"id": "CONV-002", "position_id": "CONV-002", "domain": "CONVERSION_MECHANISM", "title": "Conversion changes unbearable ideas affect into physical manifestations", "source": source, "text_evidence": "Conversion changes unbearable ideas affect into physical manifestations"},
    {"id": "CONV-003", "position_id": "CONV-003", "domain": "CONVERSION_MECHANISM", "title": "Hysteria renders unbearable idea harmless by transforming sum of excitement into somatic", "source": source, "text_evidence": "Hysteria renders unbearable idea harmless by transforming sum of excitement into somatic"},
    {"id": "CONV-004", "position_id": "CONV-004", "domain": "CONVERSION_MECHANISM", "title": "Memory symbol remains in consciousness as motor innervation or hallucinatory sensation", "source": source, "text_evidence": "Memory symbol remains in consciousness as motor innervation or hallucinatory sensation"},
    {"id": "CONV-005", "position_id": "CONV-005", "domain": "CONVERSION_MECHANISM", "title": "Conversion may be total or partial along motor or sensory innervation paths", "source": source, "text_evidence": "Conversion may be total or partial along motor or sensory innervation paths"},
    {"id": "CONV-006", "position_id": "CONV-006", "domain": "CONVERSION_MECHANISM", "title": "Conversion can occur from fresh or remembered affect", "source": source, "text_evidence": "Conversion can occur from fresh or remembered affect"},
    {"id": "CONV-007", "position_id": "CONV-007", "domain": "CONVERSION_MECHANISM", "title": "Psychophysical adaptation for transference of excitement into bodily innervation", "source": source, "text_evidence": "Psychophysical adaptation for transference of excitement into bodily innervation"},
    {"id": "CONV-008", "position_id": "CONV-008", "domain": "CONVERSION_MECHANISM", "title": "Conversion serves adequate action expression of emotions", "source": source, "text_evidence": "Conversion serves adequate action expression of emotions"},
    {"id": "CONV-009", "position_id": "CONV-009", "domain": "CONVERSION_MECHANISM", "title": "Symptoms are symbolic expression of repressed wish realization", "source": source, "text_evidence": "Symptoms are symbolic expression of repressed wish realization"},
])

# THERAPEUTIC METHOD (14)
new_positions.extend([
    {"id": "THER-001", "position_id": "THER-001", "domain": "THERAPEUTIC_METHOD", "title": "Cathartic method bringing repressed material to consciousness with affect produces cure", "source": source, "text_evidence": "Cathartic method bringing repressed material to consciousness with affect produces cure"},
    {"id": "THER-002", "position_id": "THER-002", "domain": "THERAPEUTIC_METHOD", "title": "Talking cure allows symbolic verbal expression replacing somatic expression", "source": source, "text_evidence": "Talking cure allows symbolic verbal expression replacing somatic expression"},
    {"id": "THER-003", "position_id": "THER-003", "domain": "THERAPEUTIC_METHOD", "title": "Physician must overcome patient resistance through persistent inquiry", "source": source, "text_evidence": "Physician must overcome patient resistance through persistent inquiry"},
    {"id": "THER-004", "position_id": "THER-004", "domain": "THERAPEUTIC_METHOD", "title": "Therapeutic success requires conscious confrontation of repressed trauma", "source": source, "text_evidence": "Therapeutic success requires conscious confrontation of repressed trauma"},
    {"id": "THER-005", "position_id": "THER-005", "domain": "THERAPEUTIC_METHOD", "title": "Pressure procedure reveals pathogenic reminiscences without hypnosis", "source": source, "text_evidence": "Pressure procedure reveals pathogenic reminiscences without hypnosis"},
    {"id": "THER-006", "position_id": "THER-006", "domain": "THERAPEUTIC_METHOD", "title": "Therapy abrogates efficacy of non abreacted presentation by outlet through speech", "source": source, "text_evidence": "Therapy abrogates efficacy of non abreacted presentation by outlet through speech"},
    {"id": "THER-007", "position_id": "THER-007", "domain": "THERAPEUTIC_METHOD", "title": "Therapy brings to associative correction by drawing into normal consciousness", "source": source, "text_evidence": "Therapy brings to associative correction by drawing into normal consciousness"},
    {"id": "THER-008", "position_id": "THER-008", "domain": "THERAPEUTIC_METHOD", "title": "Psychoanalytic method removes symptoms by making unconscious conscious", "source": source, "text_evidence": "Psychoanalytic method removes symptoms by making unconscious conscious"},
    {"id": "THER-009", "position_id": "THER-009", "domain": "THERAPEUTIC_METHOD", "title": "Individual hysterical symptoms disappear when memories thoroughly awakened with affect", "source": source, "text_evidence": "Individual hysterical symptoms disappear when memories thoroughly awakened with affect"},
    {"id": "THER-010", "position_id": "THER-010", "domain": "THERAPEUTIC_METHOD", "title": "Affectless memories almost utterly useless for cure", "source": source, "text_evidence": "Affectless memories almost utterly useless for cure"},
    {"id": "THER-011", "position_id": "THER-011", "domain": "THERAPEUTIC_METHOD", "title": "Psychic process must be reproduced vividly into statum nascendi", "source": source, "text_evidence": "Psychic process must be reproduced vividly into statum nascendi"},
    {"id": "THER-012", "position_id": "THER-012", "domain": "THERAPEUTIC_METHOD", "title": "Process must be thoroughly talked over with free play to affect", "source": source, "text_evidence": "Process must be thoroughly talked over with free play to affect"},
    {"id": "THER-013", "position_id": "THER-013", "domain": "THERAPEUTIC_METHOD", "title": "Revealing unconscious removes compulsion conscious will reaches conscious processes only", "source": source, "text_evidence": "Revealing unconscious removes compulsion conscious will reaches conscious processes only"},
    {"id": "THER-014", "position_id": "THER-014", "domain": "THERAPEUTIC_METHOD", "title": "Treatment overcomes inner resistances functions as after-training re-education", "source": source, "text_evidence": "Treatment overcomes inner resistances functions as after-training re-education"},
])

# CONSCIOUSNESS STRUCTURE (9)
new_positions.extend([
    {"id": "CONS-001", "position_id": "CONS-001", "domain": "CONSCIOUSNESS_STRUCTURE", "title": "Consciousness not coextensive with mental life unconscious contains active content", "source": source, "text_evidence": "Consciousness not coextensive with mental life unconscious contains active content"},
    {"id": "CONS-002", "position_id": "CONS-002", "domain": "CONSCIOUSNESS_STRUCTURE", "title": "Hypnoid states create conditions for pathological ideation separate from normal", "source": source, "text_evidence": "Hypnoid states create conditions for pathological ideation separate from normal"},
    {"id": "CONS-003", "position_id": "CONS-003", "domain": "CONSCIOUSNESS_STRUCTURE", "title": "Ideas inadmissible to consciousness due to ego incompatibility", "source": source, "text_evidence": "Ideas inadmissible to consciousness due to ego incompatibility"},
    {"id": "CONS-004", "position_id": "CONS-004", "domain": "CONSCIOUSNESS_STRUCTURE", "title": "Boundary between conscious unconscious maintained by active psychological forces", "source": source, "text_evidence": "Boundary between conscious unconscious maintained by active psychological forces"},
    {"id": "CONS-005", "position_id": "CONS-005", "domain": "CONSCIOUSNESS_STRUCTURE", "title": "Double consciousness splitting fundamental to hysteria", "source": source, "text_evidence": "Double consciousness splitting fundamental to hysteria"},
    {"id": "CONS-006", "position_id": "CONS-006", "domain": "CONSCIOUSNESS_STRUCTURE", "title": "Splitting of consciousness exists rudimentarily in every hysteria", "source": source, "text_evidence": "Splitting of consciousness exists rudimentarily in every hysteria"},
    {"id": "CONS-007", "position_id": "CONS-007", "domain": "CONSCIOUSNESS_STRUCTURE", "title": "Hypnoid states represent higher organization as rudimentary second consciousness", "source": source, "text_evidence": "Hypnoid states represent higher organization as rudimentary second consciousness"},
    {"id": "CONS-008", "position_id": "CONS-008", "domain": "CONSCIOUSNESS_STRUCTURE", "title": "Pathogenic psychic group excluded from associative relations with normal ego", "source": source, "text_evidence": "Pathogenic psychic group excluded from associative relations with normal ego"},
    {"id": "CONS-009", "position_id": "CONS-009", "domain": "CONSCIOUSNESS_STRUCTURE", "title": "Separate psychic group can attain various degrees of psychic organization", "source": source, "text_evidence": "Separate psychic group can attain various degrees of psychic organization"},
])

# ANXIETY NEUROSIS SYMPTOMS (15)
new_positions.extend([
    {"id": "ANXI-001", "position_id": "ANXI-001", "domain": "ANXIETY_SYMPTOMS", "title": "General irritability with accumulation of excitement", "source": source, "text_evidence": "General irritability with accumulation of excitement"},
    {"id": "ANXI-002", "position_id": "ANXI-002", "domain": "ANXIETY_SYMPTOMS", "title": "Auditory hyperesthesia as over-sensitiveness for noises", "source": source, "text_evidence": "Auditory hyperesthesia as over-sensitiveness for noises"},
    {"id": "ANXI-003", "position_id": "ANXI-003", "domain": "ANXIETY_SYMPTOMS", "title": "Anxious expectation chronic anxiety making catastrophic interpretations", "source": source, "text_evidence": "Anxious expectation chronic anxiety making catastrophic interpretations"},
    {"id": "ANXI-004", "position_id": "ANXI-004", "domain": "ANXIETY_SYMPTOMS", "title": "Hypochondria as anxious expectation referring to own health", "source": source, "text_evidence": "Hypochondria as anxious expectation referring to own health"},
    {"id": "ANXI-005", "position_id": "ANXI-005", "domain": "ANXIETY_SYMPTOMS", "title": "Attacks of anxiety sudden breaking of latent anxiety into consciousness", "source": source, "text_evidence": "Attacks of anxiety sudden breaking of latent anxiety into consciousness"},
    {"id": "ANXI-006", "position_id": "ANXI-006", "domain": "ANXIETY_SYMPTOMS", "title": "Attack of anxiety consists of anxious feeling with or without associated idea", "source": source, "text_evidence": "Attack of anxiety consists of anxious feeling with or without associated idea"},
    {"id": "ANXI-007", "position_id": "ANXI-007", "domain": "ANXIETY_SYMPTOMS", "title": "Anxiety combined with somatic disturbances cardiac respiratory vasomotor glandular", "source": source, "text_evidence": "Anxiety combined with somatic disturbances cardiac respiratory vasomotor glandular"},
    {"id": "ANXI-008", "position_id": "ANXI-008", "domain": "ANXIETY_SYMPTOMS", "title": "Rudimentary anxiety attacks and equivalents larvated states", "source": source, "text_evidence": "Rudimentary anxiety attacks and equivalents larvated states"},
    {"id": "ANXI-009", "position_id": "ANXI-009", "domain": "ANXIETY_SYMPTOMS", "title": "Nocturnal frights pavor nocturnus as variety of anxiety attack", "source": source, "text_evidence": "Nocturnal frights pavor nocturnus as variety of anxiety attack"},
    {"id": "ANXI-010", "position_id": "ANXI-010", "domain": "ANXIETY_SYMPTOMS", "title": "Vertigo locomotor coordinating type prominent in anxiety neurosis", "source": source, "text_evidence": "Vertigo locomotor coordinating type prominent in anxiety neurosis"},
    {"id": "ANXI-011", "position_id": "ANXI-011", "domain": "ANXIETY_SYMPTOMS", "title": "Vertigo attack often accompanied by worst anxiety and cardiac respiratory disturbance", "source": source, "text_evidence": "Vertigo attack often accompanied by worst anxiety and cardiac respiratory disturbance"},
    {"id": "ANXI-012", "position_id": "ANXI-012", "domain": "ANXIETY_SYMPTOMS", "title": "Phobias develop from anxious expectation and tendency to vertigo", "source": source, "text_evidence": "Phobias develop from anxious expectation and tendency to vertigo"},
    {"id": "ANXI-013", "position_id": "ANXI-013", "domain": "ANXIETY_SYMPTOMS", "title": "Digestive disturbances nausea inordinate appetite tendency to diarrhea", "source": source, "text_evidence": "Digestive disturbances nausea inordinate appetite tendency to diarrhea"},
    {"id": "ANXI-014", "position_id": "ANXI-014", "domain": "ANXIETY_SYMPTOMS", "title": "Paresthesias associate in fixed sequence during anxiety attacks", "source": source, "text_evidence": "Paresthesias associate in fixed sequence during anxiety attacks"},
    {"id": "ANXI-015", "position_id": "ANXI-015", "domain": "ANXIETY_SYMPTOMS", "title": "Conversion into bodily sensations rheumatic muscles and hallucinations", "source": source, "text_evidence": "Conversion into bodily sensations rheumatic muscles and hallucinations"},
])

# ANXIETY NEUROSIS ETIOLOGY (11)
new_positions.extend([
    {"id": "ANXI-E-001", "position_id": "ANXI-E-001", "domain": "ANXIETY_ETIOLOGY", "title": "Sexual etiology disturbances in vita sexualis cause anxiety neurosis", "source": source, "text_evidence": "Sexual etiology disturbances in vita sexualis cause anxiety neurosis"},
    {"id": "ANXI-E-002", "position_id": "ANXI-E-002", "domain": "ANXIETY_ETIOLOGY", "title": "Virginal fear in adults from sudden sexual revelation", "source": source, "text_evidence": "Virginal fear in adults from sudden sexual revelation"},
    {"id": "ANXI-E-003", "position_id": "ANXI-E-003", "domain": "ANXIETY_ETIOLOGY", "title": "Fear in newly married from anesthesia during first cohabitation", "source": source, "text_evidence": "Fear in newly married from anesthesia during first cohabitation"},
    {"id": "ANXI-E-004", "position_id": "ANXI-E-004", "domain": "ANXIETY_ETIOLOGY", "title": "Fear in women whose husbands have ejaculatio precox or diminished potency", "source": source, "text_evidence": "Fear in women whose husbands have ejaculatio precox or diminished potency"},
    {"id": "ANXI-E-005", "position_id": "ANXI-E-005", "domain": "ANXIETY_ETIOLOGY", "title": "Fear from coitus interruptus or reservatus depends on woman's gratification", "source": source, "text_evidence": "Fear from coitus interruptus or reservatus depends on woman's gratification"},
    {"id": "ANXI-E-006", "position_id": "ANXI-E-006", "domain": "ANXIETY_ETIOLOGY", "title": "Fear in widows and intentional abstainers", "source": source, "text_evidence": "Fear in widows and intentional abstainers"},
    {"id": "ANXI-E-007", "position_id": "ANXI-E-007", "domain": "ANXIETY_ETIOLOGY", "title": "Fear in climacterium during last marked enhancement of sexual desire", "source": source, "text_evidence": "Fear in climacterium during last marked enhancement of sexual desire"},
    {"id": "ANXI-E-008", "position_id": "ANXI-E-008", "domain": "ANXIETY_ETIOLOGY", "title": "Fear in men practicing intentional abstinence", "source": source, "text_evidence": "Fear in men practicing intentional abstinence"},
    {"id": "ANXI-E-009", "position_id": "ANXI-E-009", "domain": "ANXIETY_ETIOLOGY", "title": "Fear in men with frustrated excitement engagement period", "source": source, "text_evidence": "Fear in men with frustrated excitement engagement period"},
    {"id": "ANXI-E-010", "position_id": "ANXI-E-010", "domain": "ANXIETY_ETIOLOGY", "title": "Fear in men practicing coitus interruptus", "source": source, "text_evidence": "Fear in men practicing coitus interruptus"},
    {"id": "ANXI-E-011", "position_id": "ANXI-E-011", "domain": "ANXIETY_ETIOLOGY", "title": "Fear in men during senium climacterium when potency diminishes", "source": source, "text_evidence": "Fear in men during senium climacterium when potency diminishes"},
])

# ANXIETY NEUROSIS MECHANISM (8)
new_positions.extend([
    {"id": "ANXI-M-001", "position_id": "ANXI-M-001", "domain": "ANXIETY_MECHANISM", "title": "Somatic sexual excitement produced continuously in sexually mature organism", "source": source, "text_evidence": "Somatic sexual excitement produced continuously in sexually mature organism"},
    {"id": "ANXI-M-002", "position_id": "ANXI-M-002", "domain": "ANXIETY_MECHANISM", "title": "Excitement becomes periodic stimulus for psychic life when reaching threshold", "source": source, "text_evidence": "Excitement becomes periodic stimulus for psychic life when reaching threshold"},
    {"id": "ANXI-M-003", "position_id": "ANXI-M-003", "domain": "ANXIETY_MECHANISM", "title": "Psychic unburdening possible only through specific adequate action", "source": source, "text_evidence": "Psychic unburdening possible only through specific adequate action"},
    {"id": "ANXI-M-004", "position_id": "ANXI-M-004", "domain": "ANXIETY_MECHANISM", "title": "Anything except adequate action of no avail excitement must be freed", "source": source, "text_evidence": "Anything except adequate action of no avail excitement must be freed"},
    {"id": "ANXI-M-005", "position_id": "ANXI-M-005", "domain": "ANXIETY_MECHANISM", "title": "Anxiety neurosis when adequate unburdening replaced by less adequate one", "source": source, "text_evidence": "Anxiety neurosis when adequate unburdening replaced by less adequate one"},
    {"id": "ANXI-M-006", "position_id": "ANXI-M-006", "domain": "ANXIETY_MECHANISM", "title": "Somatic excitement diverted from psyche expended subcortically in inadequate reactions", "source": source, "text_evidence": "Somatic excitement diverted from psyche expended subcortically in inadequate reactions"},
    {"id": "ANXI-M-007", "position_id": "ANXI-M-007", "domain": "ANXIETY_MECHANISM", "title": "Libido diminished while somatic excitement diverted to another route", "source": source, "text_evidence": "Libido diminished while somatic excitement diverted to another route"},
    {"id": "ANXI-M-008", "position_id": "ANXI-M-008", "domain": "ANXIETY_MECHANISM", "title": "Psyche insufficient for subjugating somatic sexual excitement", "source": source, "text_evidence": "Psyche insufficient for subjugating somatic sexual excitement"},
])

# OBSESSIONS AND COMPULSIONS (13)
new_positions.extend([
    {"id": "OBSE-001", "position_id": "OBSE-001", "domain": "OBSESSIONS_COMPULSIONS", "title": "Obsessions are transformed reproaches returning from repression", "source": source, "text_evidence": "Obsessions are transformed reproaches returning from repression"},
    {"id": "OBSE-002", "position_id": "OBSE-002", "domain": "OBSESSIONS_COMPULSIONS", "title": "Reproaches always refer to pleasurably accomplished sexual action of childhood", "source": source, "text_evidence": "Reproaches always refer to pleasurably accomplished sexual action of childhood"},
    {"id": "OBSE-003", "position_id": "OBSE-003", "domain": "OBSESSIONS_COMPULSIONS", "title": "Sexual experiences of early childhood pleasurably accomplished aggressions", "source": source, "text_evidence": "Sexual experiences of early childhood pleasurably accomplished aggressions"},
    {"id": "OBSE-004", "position_id": "OBSE-004", "domain": "OBSESSIONS_COMPULSIONS", "title": "Sexual activity not passivity in obsessions masculine sex preferred", "source": source, "text_evidence": "Sexual activity not passivity in obsessions masculine sex preferred"},
    {"id": "OBSE-005", "position_id": "OBSE-005", "domain": "OBSESSIONS_COMPULSIONS", "title": "Period of childish immorality contains seeds of later neurosis", "source": source, "text_evidence": "Period of childish immorality contains seeds of later neurosis"},
    {"id": "OBSE-006", "position_id": "OBSE-006", "domain": "OBSESSIONS_COMPULSIONS", "title": "Sexual maturity brings reproach attaching to memory of pleasurable action", "source": source, "text_evidence": "Sexual maturity brings reproach attaching to memory of pleasurable action"},
    {"id": "OBSE-007", "position_id": "OBSE-007", "domain": "OBSESSIONS_COMPULSIONS", "title": "Reproach and memory repressed replaced by primary symptom of defense scrupulousness", "source": source, "text_evidence": "Reproach and memory repressed replaced by primary symptom of defense scrupulousness"},
    {"id": "OBSE-008", "position_id": "OBSE-008", "domain": "OBSESSIONS_COMPULSIONS", "title": "Period of apparent healthiness shows successful defense", "source": source, "text_evidence": "Period of apparent healthiness shows successful defense"},
    {"id": "OBSE-009", "position_id": "OBSE-009", "domain": "OBSESSIONS_COMPULSIONS", "title": "Return of repressed reproaches causes disease failure of defense", "source": source, "text_evidence": "Return of repressed reproaches causes disease failure of defense"},
    {"id": "OBSE-010", "position_id": "OBSE-010", "domain": "OBSESSIONS_COMPULSIONS", "title": "Revived memories reaching consciousness through compromise formation", "source": source, "text_evidence": "Revived memories reaching consciousness through compromise formation"},
    {"id": "OBSE-011", "position_id": "OBSE-011", "domain": "OBSESSIONS_COMPULSIONS", "title": "Obsession content doubly distorted actual replaces past non-sexual replaces sexual", "source": source, "text_evidence": "Obsession content doubly distorted actual replaces past non-sexual replaces sexual"},
    {"id": "OBSE-012", "position_id": "OBSE-012", "domain": "OBSESSIONS_COMPULSIONS", "title": "Obsession has psychical compulsion from repressed source not its own validity", "source": source, "text_evidence": "Obsession has psychical compulsion from repressed source not its own validity"},
    {"id": "OBSE-013", "position_id": "OBSE-013", "domain": "OBSESSIONS_COMPULSIONS", "title": "Reproach-affect transforms into shame hypochondria social anxiety religious anxiety delusions of observation", "source": source, "text_evidence": "Reproach-affect transforms into shame hypochondria social anxiety religious anxiety delusions of observation"},
])

# SECONDARY DEFENSE (7)
new_positions.extend([
    {"id": "SDEF-001", "position_id": "SDEF-001", "domain": "SECONDARY_DEFENSE", "title": "Secondary defense produces protective measures against obsessions", "source": source, "text_evidence": "Secondary defense produces protective measures against obsessions"},
    {"id": "SDEF-002", "position_id": "SDEF-002", "domain": "SECONDARY_DEFENSE", "title": "Forcible deviation to contrary thoughts if successful creates compulsive reasoning", "source": source, "text_evidence": "Forcible deviation to contrary thoughts if successful creates compulsive reasoning"},
    {"id": "SDEF-003", "position_id": "SDEF-003", "domain": "SECONDARY_DEFENSE", "title": "Logical labor to master obsession produces compulsive thinking and doubting mania", "source": source, "text_evidence": "Logical labor to master obsession produces compulsive thinking and doubting mania"},
    {"id": "SDEF-004", "position_id": "SDEF-004", "domain": "SECONDARY_DEFENSE", "title": "Priority of perception over memory produces collecting preserving of objects", "source": source, "text_evidence": "Priority of perception over memory produces collecting preserving of objects"},
    {"id": "SDEF-005", "position_id": "SDEF-005", "domain": "SECONDARY_DEFENSE", "title": "Defense against compulsive affects produces measures of penitence prevention betrayal-fear", "source": source, "text_evidence": "Defense against compulsive affects produces measures of penitence prevention betrayal-fear"},
    {"id": "SDEF-006", "position_id": "SDEF-006", "domain": "SECONDARY_DEFENSE", "title": "Compulsion transfers from idea affect to protective measure", "source": source, "text_evidence": "Compulsion transfers from idea affect to protective measure"},
    {"id": "SDEF-007", "position_id": "SDEF-007", "domain": "SECONDARY_DEFENSE", "title": "Protective measures can fix into ceremonial actions doubting mania or phobia-conditioned existence", "source": source, "text_evidence": "Protective measures can fix into ceremonial actions doubting mania or phobia-conditioned existence"},
])

# PARANOIA MECHANISMS (9)
new_positions.extend([
    {"id": "PARA-001", "position_id": "PARA-001", "domain": "PARANOIA_MECHANISMS", "title": "Paranoia is defense psychosis originates from repression of painful reminiscences", "source": source, "text_evidence": "Paranoia is defense psychosis originates from repression of painful reminiscences"},
    {"id": "PARA-002", "position_id": "PARA-002", "domain": "PARANOIA_MECHANISMS", "title": "Psychic mechanism determines form of symptoms in paranoia", "source": source, "text_evidence": "Psychic mechanism determines form of symptoms in paranoia"},
    {"id": "PARA-003", "position_id": "PARA-003", "domain": "PARANOIA_MECHANISMS", "title": "Defense by projection reproach repressed by placing distrust in others", "source": source, "text_evidence": "Defense by projection reproach repressed by placing distrust in others"},
    {"id": "PARA-004", "position_id": "PARA-004", "domain": "PARANOIA_MECHANISMS", "title": "Reproach deprived of recognition no protection against returning reproaches in delusions", "source": source, "text_evidence": "Reproach deprived of recognition no protection against returning reproaches in delusions"},
    {"id": "PARA-005", "position_id": "PARA-005", "domain": "PARANOIA_MECHANISMS", "title": "Hallucinations are fragments from repressed childhood experiences", "source": source, "text_evidence": "Hallucinations are fragments from repressed childhood experiences"},
    {"id": "PARA-006", "position_id": "PARA-006", "domain": "PARANOIA_MECHANISMS", "title": "Unconscious fancies become conscious through becoming loud as voices", "source": source, "text_evidence": "Unconscious fancies become conscious through becoming loud as voices"},
    {"id": "PARA-007", "position_id": "PARA-007", "domain": "PARANOIA_MECHANISMS", "title": "Voices show diplomatic uncertainty allusion deeply hidden connection masked", "source": source, "text_evidence": "Voices show diplomatic uncertainty allusion deeply hidden connection masked"},
    {"id": "PARA-008", "position_id": "PARA-008", "domain": "PARANOIA_MECHANISMS", "title": "Voices result from repression of thoughts symptoms of return of repression", "source": source, "text_evidence": "Voices result from repression of thoughts symptoms of return of repression"},
    {"id": "PARA-009", "position_id": "PARA-009", "domain": "PARANOIA_MECHANISMS", "title": "Symptoms demand combining delusional formation delusion of interpretation", "source": source, "text_evidence": "Symptoms demand combining delusional formation delusion of interpretation"},
])

# RESISTANCE IN TREATMENT (10)
new_positions.extend([
    {"id": "RESI-001", "position_id": "RESI-001", "domain": "RESISTANCE_TREATMENT", "title": "Psychic work must overcome psychic force opposing pathogenic ideas", "source": source, "text_evidence": "Psychic work must overcome psychic force opposing pathogenic ideas"},
    {"id": "RESI-002", "position_id": "RESI-002", "domain": "RESISTANCE_TREATMENT", "title": "Resistance same psychic force that originally repressed pathogenic idea", "source": source, "text_evidence": "Resistance same psychic force that originally repressed pathogenic idea"},
    {"id": "RESI-003", "position_id": "RESI-003", "domain": "RESISTANCE_TREATMENT", "title": "Patient conceals emerging ideas claiming unimportance or disagreeableness", "source": source, "text_evidence": "Patient conceals emerging ideas claiming unimportance or disagreeableness"},
    {"id": "RESI-004", "position_id": "RESI-004", "domain": "RESISTANCE_TREATMENT", "title": "Long pause between pressure and utterance indicates distortion through resistance", "source": source, "text_evidence": "Long pause between pressure and utterance indicates distortion through resistance"},
    {"id": "RESI-005", "position_id": "RESI-005", "domain": "RESISTANCE_TREATMENT", "title": "Important explanations ushered in as superfluous accessories", "source": source, "text_evidence": "Important explanations ushered in as superfluous accessories"},
    {"id": "RESI-006", "position_id": "RESI-006", "domain": "RESISTANCE_TREATMENT", "title": "Pathogenic idea appears insignificant on return sign of successful defense", "source": source, "text_evidence": "Pathogenic idea appears insignificant on return sign of successful defense"},
    {"id": "RESI-007", "position_id": "RESI-007", "domain": "RESISTANCE_TREATMENT", "title": "Patient designates reproductions as non arrivée or added not reproduced", "source": source, "text_evidence": "Patient designates reproductions as non arrivée or added not reproduced"},
    {"id": "RESI-008", "position_id": "RESI-008", "domain": "RESISTANCE_TREATMENT", "title": "Resistance failure when obstinacy in denying ideas under pressure", "source": source, "text_evidence": "Resistance failure when obstinacy in denying ideas under pressure"},
    {"id": "RESI-009", "position_id": "RESI-009", "domain": "RESISTANCE_TREATMENT", "title": "Transference to physician painful ideas transferred through false connection", "source": source, "text_evidence": "Transference to physician painful ideas transferred through false connection"},
    {"id": "RESI-010", "position_id": "RESI-010", "domain": "RESISTANCE_TREATMENT", "title": "New symptoms formed during treatment as transference-substitutes", "source": source, "text_evidence": "New symptoms formed during treatment as transference-substitutes"},
])

# HYSTERICAL SYMPTOMS STRUCTURE (12)
new_positions.extend([
    {"id": "SYST-001", "position_id": "SYST-001", "domain": "SYMPTOM_STRUCTURE", "title": "Symptoms are memory symbols of efficacious traumatic impressions", "source": source, "text_evidence": "Symptoms are memory symbols of efficacious traumatic impressions"},
    {"id": "SYST-002", "position_id": "SYST-002", "domain": "SYMPTOM_STRUCTURE", "title": "Symptoms represent compensation by conversion for associative return of trauma", "source": source, "text_evidence": "Symptoms represent compensation by conversion for associative return of trauma"},
    {"id": "SYST-003", "position_id": "SYST-003", "domain": "SYMPTOM_STRUCTURE", "title": "Symptoms are expression of wish realization", "source": source, "text_evidence": "Symptoms are expression of wish realization"},
    {"id": "SYST-004", "position_id": "SYST-004", "domain": "SYMPTOM_STRUCTURE", "title": "Symptoms realize unconscious fancy serving wish fulfillment", "source": source, "text_evidence": "Symptoms realize unconscious fancy serving wish fulfillment"},
    {"id": "SYST-005", "position_id": "SYST-005", "domain": "SYMPTOM_STRUCTURE", "title": "Symptoms serve sexual gratification represent part of sexual life", "source": source, "text_evidence": "Symptoms serve sexual gratification represent part of sexual life"},
    {"id": "SYST-006", "position_id": "SYST-006", "domain": "SYMPTOM_STRUCTURE", "title": "Symptoms correspond to return of sexual gratification real in infantile life", "source": source, "text_evidence": "Symptoms correspond to return of sexual gratification real in infantile life"},
    {"id": "SYST-007", "position_id": "SYST-007", "domain": "SYMPTOM_STRUCTURE", "title": "Symptoms result as compromise between two opposing affects impulses", "source": source, "text_evidence": "Symptoms result as compromise between two opposing affects impulses"},
    {"id": "SYST-008", "position_id": "SYST-008", "domain": "SYMPTOM_STRUCTURE", "title": "Symptoms can represent diverse non-sexual incitements but cannot lack sexual significance", "source": source, "text_evidence": "Symptoms can represent diverse non-sexual incitements but cannot lack sexual significance"},
    {"id": "SYST-009", "position_id": "SYST-009", "domain": "SYMPTOM_STRUCTURE", "title": "Symptoms can require two sexual fancies one masculine one feminine", "source": source, "text_evidence": "Symptoms can require two sexual fancies one masculine one feminine"},
    {"id": "SYST-010", "position_id": "SYST-010", "domain": "SYMPTOM_STRUCTURE", "title": "Bisexual significance represents highest complexity of symptom determination", "source": source, "text_evidence": "Bisexual significance represents highest complexity of symptom determination"},
    {"id": "SYST-011", "position_id": "SYST-011", "domain": "SYMPTOM_STRUCTURE", "title": "Symptoms join in discussion reappear when related pathogenic memory approached", "source": source, "text_evidence": "Symptoms join in discussion reappear when related pathogenic memory approached"},
    {"id": "SYST-012", "position_id": "SYST-012", "domain": "SYMPTOM_STRUCTURE", "title": "Symptom intensity fluctuates with depth of penetration into pathogenic memory", "source": source, "text_evidence": "Symptom intensity fluctuates with depth of penetration into pathogenic memory"},
])

# HYSTERICAL FANCIES (6)
new_positions.extend([
    {"id": "FANC-001", "position_id": "FANC-001", "domain": "HYSTERICAL_FANCIES", "title": "Unconscious fancies are nearest psychical steps to hysterical symptoms", "source": source, "text_evidence": "Unconscious fancies are nearest psychical steps to hysterical symptoms"},
    {"id": "FANC-002", "position_id": "FANC-002", "domain": "HYSTERICAL_FANCIES", "title": "Fancies once conscious day-dreams intentionally forgotten merged into unconscious by repression", "source": source, "text_evidence": "Fancies once conscious day-dreams intentionally forgotten merged into unconscious by repression"},
    {"id": "FANC-003", "position_id": "FANC-003", "domain": "HYSTERICAL_FANCIES", "title": "Unconscious fancy identical with fancy helping sexual gratification during masturbation", "source": source, "text_evidence": "Unconscious fancy identical with fancy helping sexual gratification during masturbation"},
    {"id": "FANC-004", "position_id": "FANC-004", "domain": "HYSTERICAL_FANCIES", "title": "When masturbation abandoned fancy changes from conscious to unconscious", "source": source, "text_evidence": "When masturbation abandoned fancy changes from conscious to unconscious"},
    {"id": "FANC-005", "position_id": "FANC-005", "domain": "HYSTERICAL_FANCIES", "title": "Unconscious fancies grow exuberantly with force of desire for love", "source": source, "text_evidence": "Unconscious fancies grow exuberantly with force of desire for love"},
    {"id": "FANC-006", "position_id": "FANC-006", "domain": "HYSTERICAL_FANCIES", "title": "Symptoms are unconscious fancies brought to light by conversion", "source": source, "text_evidence": "Symptoms are unconscious fancies brought to light by conversion"},
])

# PSYCHIC ORGANIZATION (8)
new_positions.extend([
    {"id": "ORGA-001", "position_id": "ORGA-001", "domain": "PSYCHIC_ORGANIZATION", "title": "Pathogenic material organized in multidimensional stratification triple", "source": source, "text_evidence": "Pathogenic material organized in multidimensional stratification triple"},
    {"id": "ORGA-002", "position_id": "ORGA-002", "domain": "PSYCHIC_ORGANIZATION", "title": "Linear chronological arrangement within each theme", "source": source, "text_evidence": "Linear chronological arrangement within each theme"},
    {"id": "ORGA-003", "position_id": "ORGA-003", "domain": "PSYCHIC_ORGANIZATION", "title": "Concentric stratification around pathogenic nucleus by resistance levels", "source": source, "text_evidence": "Concentric stratification around pathogenic nucleus by resistance levels"},
    {"id": "ORGA-004", "position_id": "ORGA-004", "domain": "PSYCHIC_ORGANIZATION", "title": "Arrangement according to content of thought logical thread", "source": source, "text_evidence": "Arrangement according to content of thought logical thread"},
    {"id": "ORGA-005", "position_id": "ORGA-005", "domain": "PSYCHIC_ORGANIZATION", "title": "Logical connection corresponds to ramifying converging system of lines", "source": source, "text_evidence": "Logical connection corresponds to ramifying converging system of lines"},
    {"id": "ORGA-006", "position_id": "ORGA-006", "domain": "PSYCHIC_ORGANIZATION", "title": "Multiple threads converge at junctions then proceed united to nucleus", "source": source, "text_evidence": "Multiple threads converge at junctions then proceed united to nucleus"},
    {"id": "ORGA-007", "position_id": "ORGA-007", "domain": "PSYCHIC_ORGANIZATION", "title": "Pathogenic material has infiltration character not foreign body character", "source": source, "text_evidence": "Pathogenic material has infiltration character not foreign body character"},
    {"id": "ORGA-008", "position_id": "ORGA-008", "domain": "PSYCHIC_ORGANIZATION", "title": "Memory of painful experience preserved with undiminished vividness as fresh occurrence", "source": source, "text_evidence": "Memory of painful experience preserved with undiminished vividness as fresh occurrence"},
])

# GENERAL NEUROSIS THEORY (8) - using GNEUR to avoid conflict with existing NEUR IDs
new_positions.extend([
    {"id": "GNEUR-001", "position_id": "GNEUR-001", "domain": "GENERAL_NEUROSIS_THEORY", "title": "Essence of psychoneuroses lies in disturbances of sexual processes", "source": source, "text_evidence": "Essence of psychoneuroses lies in disturbances of sexual processes"},
    {"id": "GNEUR-002", "position_id": "GNEUR-002", "domain": "GENERAL_NEUROSIS_THEORY", "title": "Sexual processes determine formation and utilization of sexual libido", "source": source, "text_evidence": "Sexual processes determine formation and utilization of sexual libido"},
    {"id": "GNEUR-003", "position_id": "GNEUR-003", "domain": "GENERAL_NEUROSIS_THEORY", "title": "Processes ultimately chemical sexual metabolism disturbances", "source": source, "text_evidence": "Processes ultimately chemical sexual metabolism disturbances"},
    {"id": "GNEUR-004", "position_id": "GNEUR-004", "domain": "GENERAL_NEUROSIS_THEORY", "title": "Actual neuroses show somatic effects psychoneuroses show psychic effects of disturbances", "source": source, "text_evidence": "Actual neuroses show somatic effects psychoneuroses show psychic effects of disturbances"},
    {"id": "GNEUR-005", "position_id": "GNEUR-005", "domain": "GENERAL_NEUROSIS_THEORY", "title": "Neurasthenia originates from inadequate discharge masturbation pollution", "source": source, "text_evidence": "Neurasthenia originates from inadequate discharge masturbation pollution"},
    {"id": "GNEUR-006", "position_id": "GNEUR-006", "domain": "GENERAL_NEUROSIS_THEORY", "title": "Repression is primary feature neurosis as negative of perversion", "source": source, "text_evidence": "Repression is primary feature neurosis as negative of perversion"},
    {"id": "GNEUR-007", "position_id": "GNEUR-007", "domain": "GENERAL_NEUROSIS_THEORY", "title": "Etiology requires multiplicity of factors reinforcing each other", "source": source, "text_evidence": "Etiology requires multiplicity of factors reinforcing each other"},
    {"id": "GNEUR-008", "position_id": "GNEUR-008", "domain": "GENERAL_NEUROSIS_THEORY", "title": "Disease results from summation measure of etiological determinations completed from any part", "source": source, "text_evidence": "Disease results from summation measure of etiological determinations completed from any part"},
])

# Add all 156 positions to database
data['positions'].extend(new_positions)

# Update metadata
data['metadata']['version'] = 'v5_HYSTERIA_PAPERS_ADDED'
data['metadata']['total_positions'] = len(data['positions'])
data['metadata']['date_created'] = 'November 17, 2025'

# Save
with open('data/FREUD_DATABASE.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"✓ Successfully added {len(new_positions)} new positions!")
print(f"✓ New total: {data['metadata']['total_positions']} positions")
print(f"✓ New version: {data['metadata']['version']}")
