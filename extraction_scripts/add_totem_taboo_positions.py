import json

# Load current database
with open('data/FREUD_DATABASE.json', 'r') as f:
    data = json.load(f)

print(f"Current positions: {len(data['positions'])}")

source = ["Totem and Taboo (1913)"]

# ALL 253 POSITIONS FOR WORK-006
new_positions = []

# WORK_006 (0)
new_positions.extend([
])

# TOTEMISM_FUNDAMENTALS (12)
new_positions.extend([
    {"id": "TOTM-001", "position_id": "TOTM-001", "domain": "TOTEMISM_FUNDAMENTALS", "title": "Totem is simultaneously tribal ancestor and tutelary spirit protecting the clan", "source": source, "text_evidence": "Totem is simultaneously tribal ancestor and tutelary spirit protecting the clan"},
    {"id": "TOTM-002", "position_id": "TOTM-002", "domain": "TOTEMISM_FUNDAMENTALS", "title": "Totem animal must not be killed or eaten by clan members", "source": source, "text_evidence": "Totem animal must not be killed or eaten by clan members"},
    {"id": "TOTM-003", "position_id": "TOTM-003", "domain": "TOTEMISM_FUNDAMENTALS", "title": "Totem identity is hereditary through maternal or paternal line", "source": source, "text_evidence": "Totem identity is hereditary through maternal or paternal line"},
    {"id": "TOTM-004", "position_id": "TOTM-004", "domain": "TOTEMISM_FUNDAMENTALS", "title": "Totem transcends tribal relationship and supersedes consanguineous bonds", "source": source, "text_evidence": "Totem transcends tribal relationship and supersedes consanguineous bonds"},
    {"id": "TOTM-005", "position_id": "TOTM-005", "domain": "TOTEMISM_FUNDAMENTALS", "title": "Members of same totem forbidden from sexual intercourse (exogamy)", "source": source, "text_evidence": "Members of same totem forbidden from sexual intercourse (exogamy)"},
    {"id": "TOTM-006", "position_id": "TOTM-006", "domain": "TOTEMISM_FUNDAMENTALS", "title": "Totem violations punished automatically by severe illness or death", "source": source, "text_evidence": "Totem violations punished automatically by severe illness or death"},
    {"id": "TOTM-007", "position_id": "TOTM-007", "domain": "TOTEMISM_FUNDAMENTALS", "title": "Totem animal occasionally raised and cared for in captivity", "source": source, "text_evidence": "Totem animal occasionally raised and cared for in captivity"},
    {"id": "TOTM-008", "position_id": "TOTM-008", "domain": "TOTEMISM_FUNDAMENTALS", "title": "Dead totem animal mourned and buried like clan member", "source": source, "text_evidence": "Dead totem animal mourned and buried like clan member"},
    {"id": "TOTM-009", "position_id": "TOTM-009", "domain": "TOTEMISM_FUNDAMENTALS", "title": "Totem provides protection, warnings, and premonitions to clan", "source": source, "text_evidence": "Totem provides protection, warnings, and premonitions to clan"},
    {"id": "TOTM-010", "position_id": "TOTM-010", "domain": "TOTEMISM_FUNDAMENTALS", "title": "Identification with totem expressed through disguise, imitation, naming", "source": source, "text_evidence": "Identification with totem expressed through disguise, imitation, naming"},
    {"id": "TOTM-011", "position_id": "TOTM-011", "domain": "TOTEMISM_FUNDAMENTALS", "title": "Totem ceremonially killed and eaten on solemn occasions", "source": source, "text_evidence": "Totem ceremonially killed and eaten on solemn occasions"},
    {"id": "TOTM-012", "position_id": "TOTM-012", "domain": "TOTEMISM_FUNDAMENTALS", "title": "Social and religious sides of totemism originally inseparable", "source": source, "text_evidence": "Social and religious sides of totemism originally inseparable"},
])

# INCEST_PROHIBITION (14)
new_positions.extend([
    {"id": "INCE-001", "position_id": "INCE-001", "domain": "INCEST_PROHIBITION", "title": "Primitive races show extraordinary incest dread despite apparent sexual freedom", "source": source, "text_evidence": "Primitive races show extraordinary incest dread despite apparent sexual freedom"},
    {"id": "INCE-002", "position_id": "INCE-002", "domain": "INCEST_PROHIBITION", "title": "Exogamy prevents sexual relations between same totem members", "source": source, "text_evidence": "Exogamy prevents sexual relations between same totem members"},
    {"id": "INCE-003", "position_id": "INCE-003", "domain": "INCEST_PROHIBITION", "title": "Totem exogamy extends beyond blood relations to entire clan group", "source": source, "text_evidence": "Totem exogamy extends beyond blood relations to entire clan group"},
    {"id": "INCE-004", "position_id": "INCE-004", "domain": "INCEST_PROHIBITION", "title": "Marriage class systems create additional incest restrictions beyond totem", "source": source, "text_evidence": "Marriage class systems create additional incest restrictions beyond totem"},
    {"id": "INCE-005", "position_id": "INCE-005", "domain": "INCEST_PROHIBITION", "title": "Avoidance customs between relatives express incest prevention", "source": source, "text_evidence": "Avoidance customs between relatives express incest prevention"},
    {"id": "INCE-006", "position_id": "INCE-006", "domain": "INCEST_PROHIBITION", "title": "Mother-in-law avoidance universally severe among totemic races", "source": source, "text_evidence": "Mother-in-law avoidance universally severe among totemic races"},
    {"id": "INCE-007", "position_id": "INCE-007", "domain": "INCEST_PROHIBITION", "title": "Brother-sister avoidance enforced from puberty onward", "source": source, "text_evidence": "Brother-sister avoidance enforced from puberty onward"},
    {"id": "INCE-008", "position_id": "INCE-008", "domain": "INCEST_PROHIBITION", "title": "Avoidance rules protect against unconscious incestuous temptation", "source": source, "text_evidence": "Avoidance rules protect against unconscious incestuous temptation"},
    {"id": "INCE-009", "position_id": "INCE-009", "domain": "INCEST_PROHIBITION", "title": "Instinctive aversion to incest theory inadequate to explain taboo intensity", "source": source, "text_evidence": "Instinctive aversion to incest theory inadequate to explain taboo intensity"},
    {"id": "INCE-010", "position_id": "INCE-010", "domain": "INCEST_PROHIBITION", "title": "Biological harm theory insufficient for primitive incest dread", "source": source, "text_evidence": "Biological harm theory insufficient for primitive incest dread"},
    {"id": "INCE-011", "position_id": "INCE-011", "domain": "INCEST_PROHIBITION", "title": "Incest prohibition implies strong unconscious incestuous desires", "source": source, "text_evidence": "Incest prohibition implies strong unconscious incestuous desires"},
    {"id": "INCE-012", "position_id": "INCE-012", "domain": "INCEST_PROHIBITION", "title": "Law forbids what instincts incline men to do", "source": source, "text_evidence": "Law forbids what instincts incline men to do"},
    {"id": "INCE-013", "position_id": "INCE-013", "domain": "INCEST_PROHIBITION", "title": "Exogamy represents first moral restriction and renunciation", "source": source, "text_evidence": "Exogamy represents first moral restriction and renunciation"},
    {"id": "INCE-014", "position_id": "INCE-014", "domain": "INCEST_PROHIBITION", "title": "Child's first sexual impulses are regularly incestuous nature", "source": source, "text_evidence": "Child's first sexual impulses are regularly incestuous nature"},
])

# TABOO_PSYCHOLOGY (16)
new_positions.extend([
    {"id": "TABO-001", "position_id": "TABO-001", "domain": "TABOO_PSYCHOLOGY", "title": "Taboo means simultaneously sacred/consecrated and dangerous/unclean/forbidden", "source": source, "text_evidence": "Taboo means simultaneously sacred/consecrated and dangerous/unclean/forbidden"},
    {"id": "TABO-002", "position_id": "TABO-002", "domain": "TABOO_PSYCHOLOGY", "title": "Taboo expresses itself essentially in prohibitions and restrictions", "source": source, "text_evidence": "Taboo expresses itself essentially in prohibitions and restrictions"},
    {"id": "TABO-003", "position_id": "TABO-003", "domain": "TABOO_PSYCHOLOGY", "title": "Taboo prohibitions lack rational justification and unknown origin", "source": source, "text_evidence": "Taboo prohibitions lack rational justification and unknown origin"},
    {"id": "TABO-004", "position_id": "TABO-004", "domain": "TABOO_PSYCHOLOGY", "title": "Taboo assumes dangerous power transmitted by contact like contagion", "source": source, "text_evidence": "Taboo assumes dangerous power transmitted by contact like contagion"},
    {"id": "TABO-005", "position_id": "TABO-005", "domain": "TABOO_PSYCHOLOGY", "title": "Violator of taboo becomes taboo himself through dangerous absorption", "source": source, "text_evidence": "Violator of taboo becomes taboo himself through dangerous absorption"},
    {"id": "TABO-006", "position_id": "TABO-006", "domain": "TABOO_PSYCHOLOGY", "title": "Taboo restrictions protect important persons and protect weak from powerful", "source": source, "text_evidence": "Taboo restrictions protect important persons and protect weak from powerful"},
    {"id": "TABO-007", "position_id": "TABO-007", "domain": "TABOO_PSYCHOLOGY", "title": "Taboo based on forbidden action for which strong unconscious inclination exists", "source": source, "text_evidence": "Taboo based on forbidden action for which strong unconscious inclination exists"},
    {"id": "TABO-008", "position_id": "TABO-008", "domain": "TABOO_PSYCHOLOGY", "title": "Taboo origin lies in ambivalent emotional attitude toward object", "source": source, "text_evidence": "Taboo origin lies in ambivalent emotional attitude toward object"},
    {"id": "TABO-009", "position_id": "TABO-009", "domain": "TABOO_PSYCHOLOGY", "title": "Taboo comparable to compulsion neurosis in motivation and mechanism", "source": source, "text_evidence": "Taboo comparable to compulsion neurosis in motivation and mechanism"},
    {"id": "TABO-010", "position_id": "TABO-010", "domain": "TABOO_PSYCHOLOGY", "title": "Unconscious hostility exists behind excessive conscious tenderness", "source": source, "text_evidence": "Unconscious hostility exists behind excessive conscious tenderness"},
    {"id": "TABO-011", "position_id": "TABO-011", "domain": "TABOO_PSYCHOLOGY", "title": "Taboo uses projection to externalize inner psychic conflicts", "source": source, "text_evidence": "Taboo uses projection to externalize inner psychic conflicts"},
    {"id": "TABO-012", "position_id": "TABO-012", "domain": "TABOO_PSYCHOLOGY", "title": "Touching prohibition nucleus of both taboo and compulsion neurosis", "source": source, "text_evidence": "Touching prohibition nucleus of both taboo and compulsion neurosis"},
    {"id": "TABO-013", "position_id": "TABO-013", "domain": "TABOO_PSYCHOLOGY", "title": "Taboo creates ceremonial actions as compromise formations", "source": source, "text_evidence": "Taboo creates ceremonial actions as compromise formations"},
    {"id": "TABO-014", "position_id": "TABO-014", "domain": "TABOO_PSYCHOLOGY", "title": "Contagion property of taboo reflects displacement of unconscious impulses", "source": source, "text_evidence": "Contagion property of taboo reflects displacement of unconscious impulses"},
    {"id": "TABO-015", "position_id": "TABO-015", "domain": "TABOO_PSYCHOLOGY", "title": "Expiation and purification ceremonies relieve taboo violations", "source": source, "text_evidence": "Expiation and purification ceremonies relieve taboo violations"},
    {"id": "TABO-016", "position_id": "TABO-016", "domain": "TABOO_PSYCHOLOGY", "title": "Taboo of dead reflects ambivalence toward deceased persons", "source": source, "text_evidence": "Taboo of dead reflects ambivalence toward deceased persons"},
])

# ENEMY_TABOO (8)
new_positions.extend([
    {"id": "ENEM-001", "position_id": "ENEM-001", "domain": "ENEMY_TABOO", "title": "Killing enemy requires reconciliation ceremonies with slain", "source": source, "text_evidence": "Killing enemy requires reconciliation ceremonies with slain"},
    {"id": "ENEM-002", "position_id": "ENEM-002", "domain": "ENEMY_TABOO", "title": "Manslayers subject to severe restrictions and purifications", "source": source, "text_evidence": "Manslayers subject to severe restrictions and purifications"},
    {"id": "ENEM-003", "position_id": "ENEM-003", "domain": "ENEMY_TABOO", "title": "Victorious warriors temporarily isolated from community", "source": source, "text_evidence": "Victorious warriors temporarily isolated from community"},
    {"id": "ENEM-004", "position_id": "ENEM-004", "domain": "ENEMY_TABOO", "title": "Slayer's dietary and behavioral restrictions follow fixed ceremonial", "source": source, "text_evidence": "Slayer's dietary and behavioral restrictions follow fixed ceremonial"},
    {"id": "ENEM-005", "position_id": "ENEM-005", "domain": "ENEMY_TABOO", "title": "Enemy's severed head treated with tenderness and respect", "source": source, "text_evidence": "Enemy's severed head treated with tenderness and respect"},
    {"id": "ENEM-006", "position_id": "ENEM-006", "domain": "ENEMY_TABOO", "title": "Mourning for slain enemy expresses ambivalent feelings", "source": source, "text_evidence": "Mourning for slain enemy expresses ambivalent feelings"},
    {"id": "ENEM-007", "position_id": "ENEM-007", "domain": "ENEMY_TABOO", "title": "Restrictions protect against spirit vengeance of deceased enemy", "source": source, "text_evidence": "Restrictions protect against spirit vengeance of deceased enemy"},
    {"id": "ENEM-008", "position_id": "ENEM-008", "domain": "ENEMY_TABOO", "title": "Manslayer taboo reveals remorse and bad conscience for killing", "source": source, "text_evidence": "Manslayer taboo reveals remorse and bad conscience for killing"},
])

# RULER_TABOO (11)
new_positions.extend([
    {"id": "RULE-001", "position_id": "RULE-001", "domain": "RULER_TABOO", "title": "Kings and chiefs both guarded and guarded against through taboo", "source": source, "text_evidence": "Kings and chiefs both guarded and guarded against through taboo"},
    {"id": "RULE-002", "position_id": "RULE-002", "domain": "RULER_TABOO", "title": "Rulers possess dangerous magic power transmissible by contact", "source": source, "text_evidence": "Rulers possess dangerous magic power transmissible by contact"},
    {"id": "RULE-003", "position_id": "RULE-003", "domain": "RULER_TABOO", "title": "Royal touch can heal but common touch of king brings danger", "source": source, "text_evidence": "Royal touch can heal but common touch of king brings danger"},
    {"id": "RULE-004", "position_id": "RULE-004", "domain": "RULER_TABOO", "title": "Rulers credited with control over nature and cosmic processes", "source": source, "text_evidence": "Rulers credited with control over nature and cosmic processes"},
    {"id": "RULE-005", "position_id": "RULE-005", "domain": "RULER_TABOO", "title": "Kings subject to oppressive ceremonial restrictions and prohibitions", "source": source, "text_evidence": "Kings subject to oppressive ceremonial restrictions and prohibitions"},
    {"id": "RULE-006", "position_id": "RULE-006", "domain": "RULER_TABOO", "title": "Taboo ceremonial simultaneously elevates and imprisons ruler", "source": source, "text_evidence": "Taboo ceremonial simultaneously elevates and imprisons ruler"},
    {"id": "RULE-007", "position_id": "RULE-007", "domain": "RULER_TABOO", "title": "Ruler taboos reveal unconscious hostility masked by veneration", "source": source, "text_evidence": "Ruler taboos reveal unconscious hostility masked by veneration"},
    {"id": "RULE-008", "position_id": "RULE-008", "domain": "RULER_TABOO", "title": "Excessive tenderness toward rulers indicates underlying hostile impulses", "source": source, "text_evidence": "Excessive tenderness toward rulers indicates underlying hostile impulses"},
    {"id": "RULE-009", "position_id": "RULE-009", "domain": "RULER_TABOO", "title": "Kings made responsible for all misfortunes through projected omnipotence", "source": source, "text_evidence": "Kings made responsible for all misfortunes through projected omnipotence"},
    {"id": "RULE-010", "position_id": "RULE-010", "domain": "RULER_TABOO", "title": "Violation of ruler's power reflects infantile attitude to father", "source": source, "text_evidence": "Violation of ruler's power reflects infantile attitude to father"},
    {"id": "RULE-011", "position_id": "RULE-011", "domain": "RULER_TABOO", "title": "Ceremonial restrictions serve as punishment and revenge on rulers", "source": source, "text_evidence": "Ceremonial restrictions serve as punishment and revenge on rulers"},
])

# DEAD_TABOO (13)
new_positions.extend([
    {"id": "DEAD-001", "position_id": "DEAD-001", "domain": "DEAD_TABOO", "title": "Dead are powerful rulers and regarded as enemies", "source": source, "text_evidence": "Dead are powerful rulers and regarded as enemies"},
    {"id": "DEAD-002", "position_id": "DEAD-002", "domain": "DEAD_TABOO", "title": "Contact with corpse renders person unclean requiring isolation", "source": source, "text_evidence": "Contact with corpse renders person unclean requiring isolation"},
    {"id": "DEAD-003", "position_id": "DEAD-003", "domain": "DEAD_TABOO", "title": "Mourners subject to severe dietary and behavioral restrictions", "source": source, "text_evidence": "Mourners subject to severe dietary and behavioral restrictions"},
    {"id": "DEAD-004", "position_id": "DEAD-004", "domain": "DEAD_TABOO", "title": "Name of deceased forbidden to pronounce for extended period", "source": source, "text_evidence": "Name of deceased forbidden to pronounce for extended period"},
    {"id": "DEAD-005", "position_id": "DEAD-005", "domain": "DEAD_TABOO", "title": "Name avoidance may require vocabulary changes in tribe", "source": source, "text_evidence": "Name avoidance may require vocabulary changes in tribe"},
    {"id": "DEAD-006", "position_id": "DEAD-006", "domain": "DEAD_TABOO", "title": "Dead person's spirit considered hostile and vengeful", "source": source, "text_evidence": "Dead person's spirit considered hostile and vengeful"},
    {"id": "DEAD-007", "position_id": "DEAD-007", "domain": "DEAD_TABOO", "title": "Spirits of dead hover near survivors seeking to harm them", "source": source, "text_evidence": "Spirits of dead hover near survivors seeking to harm them"},
    {"id": "DEAD-008", "position_id": "DEAD-008", "domain": "DEAD_TABOO", "title": "Survivor's ambivalence projects hostility onto dead person's spirit", "source": source, "text_evidence": "Survivor's ambivalence projects hostility onto dead person's spirit"},
    {"id": "DEAD-009", "position_id": "DEAD-009", "domain": "DEAD_TABOO", "title": "Unconscious hostile wishes toward deceased create guilt and fear", "source": source, "text_evidence": "Unconscious hostile wishes toward deceased create guilt and fear"},
    {"id": "DEAD-010", "position_id": "DEAD-010", "domain": "DEAD_TABOO", "title": "Mourning represents conflict between grief and unconscious satisfaction", "source": source, "text_evidence": "Mourning represents conflict between grief and unconscious satisfaction"},
    {"id": "DEAD-011", "position_id": "DEAD-011", "domain": "DEAD_TABOO", "title": "Defensive projection transforms inner hostility into external threat", "source": source, "text_evidence": "Defensive projection transforms inner hostility into external threat"},
    {"id": "DEAD-012", "position_id": "DEAD-012", "domain": "DEAD_TABOO", "title": "Taboo of dead originates in opposition of grief and unconscious hostility", "source": source, "text_evidence": "Taboo of dead originates in opposition of grief and unconscious hostility"},
    {"id": "DEAD-013", "position_id": "DEAD-013", "domain": "DEAD_TABOO", "title": "Death transforms beloved person into demon through ambivalence", "source": source, "text_evidence": "Death transforms beloved person into demon through ambivalence"},
])

# AMBIVALENCE_THEORY (10)
new_positions.extend([
    {"id": "AMBI-001", "position_id": "AMBI-001", "domain": "AMBIVALENCE_THEORY", "title": "Ambivalence is simultaneous love and hate toward same object", "source": source, "text_evidence": "Ambivalence is simultaneous love and hate toward same object"},
    {"id": "AMBI-002", "position_id": "AMBI-002", "domain": "AMBIVALENCE_THEORY", "title": "Ambivalent feelings universal in father-child relationships", "source": source, "text_evidence": "Ambivalent feelings universal in father-child relationships"},
    {"id": "AMBI-003", "position_id": "AMBI-003", "domain": "AMBIVALENCE_THEORY", "title": "Compulsion neurosis characterized by extreme ambivalence", "source": source, "text_evidence": "Compulsion neurosis characterized by extreme ambivalence"},
    {"id": "AMBI-004", "position_id": "AMBI-004", "domain": "AMBIVALENCE_THEORY", "title": "Ambivalence creates need for taboo prohibitions and restrictions", "source": source, "text_evidence": "Ambivalence creates need for taboo prohibitions and restrictions"},
    {"id": "AMBI-005", "position_id": "AMBI-005", "domain": "AMBIVALENCE_THEORY", "title": "One component of ambivalence usually unconscious requiring repression", "source": source, "text_evidence": "One component of ambivalence usually unconscious requiring repression"},
    {"id": "AMBI-006", "position_id": "AMBI-006", "domain": "AMBIVALENCE_THEORY", "title": "Excessive tenderness indicates reaction-formation against unconscious hate", "source": source, "text_evidence": "Excessive tenderness indicates reaction-formation against unconscious hate"},
    {"id": "AMBI-007", "position_id": "AMBI-007", "domain": "AMBIVALENCE_THEORY", "title": "Hostile component of ambivalence projected outward in primitive thought", "source": source, "text_evidence": "Hostile component of ambivalence projected outward in primitive thought"},
    {"id": "AMBI-008", "position_id": "AMBI-008", "domain": "AMBIVALENCE_THEORY", "title": "Ambivalence toward father model for all later authority relations", "source": source, "text_evidence": "Ambivalence toward father model for all later authority relations"},
    {"id": "AMBI-009", "position_id": "AMBI-009", "domain": "AMBIVALENCE_THEORY", "title": "Cultural evolution shows gradual abatement of ambivalent intensity", "source": source, "text_evidence": "Cultural evolution shows gradual abatement of ambivalent intensity"},
    {"id": "AMBI-010", "position_id": "AMBI-010", "domain": "AMBIVALENCE_THEORY", "title": "Neurotic preserves archaic ambivalence as constitutional remnant", "source": source, "text_evidence": "Neurotic preserves archaic ambivalence as constitutional remnant"},
])

# ANIMISM_FUNDAMENTALS (12)
new_positions.extend([
    {"id": "ANIM-001", "position_id": "ANIM-001", "domain": "ANIMISM_FUNDAMENTALS", "title": "Animism is theory of psychic/spiritual beings inhabiting world", "source": source, "text_evidence": "Animism is theory of psychic/spiritual beings inhabiting world"},
    {"id": "ANIM-002", "position_id": "ANIM-002", "domain": "ANIMISM_FUNDAMENTALS", "title": "Primitive man populates world with multitude of spirits", "source": source, "text_evidence": "Primitive man populates world with multitude of spirits"},
    {"id": "ANIM-003", "position_id": "ANIM-003", "domain": "ANIMISM_FUNDAMENTALS", "title": "Soul conceived as independent entity capable of leaving body", "source": source, "text_evidence": "Soul conceived as independent entity capable of leaving body"},
    {"id": "ANIM-004", "position_id": "ANIM-004", "domain": "ANIMISM_FUNDAMENTALS", "title": "Soul conceptions originate from dream and death phenomena", "source": source, "text_evidence": "Soul conceptions originate from dream and death phenomena"},
    {"id": "ANIM-005", "position_id": "ANIM-005", "domain": "ANIMISM_FUNDAMENTALS", "title": "Animism represents first complete world-system of mankind", "source": source, "text_evidence": "Animism represents first complete world-system of mankind"},
    {"id": "ANIM-006", "position_id": "ANIM-006", "domain": "ANIMISM_FUNDAMENTALS", "title": "Three world-systems: animistic, religious, scientific", "source": source, "text_evidence": "Three world-systems: animistic, religious, scientific"},
    {"id": "ANIM-007", "position_id": "ANIM-007", "domain": "ANIMISM_FUNDAMENTALS", "title": "Animism most consistent and exhaustive explanatory system", "source": source, "text_evidence": "Animism most consistent and exhaustive explanatory system"},
    {"id": "ANIM-008", "position_id": "ANIM-008", "domain": "ANIMISM_FUNDAMENTALS", "title": "Spirit projections represent externalized psychic processes", "source": source, "text_evidence": "Spirit projections represent externalized psychic processes"},
    {"id": "ANIM-009", "position_id": "ANIM-009", "domain": "ANIMISM_FUNDAMENTALS", "title": "Belief in souls reflects recognition of unconscious mental processes", "source": source, "text_evidence": "Belief in souls reflects recognition of unconscious mental processes"},
    {"id": "ANIM-010", "position_id": "ANIM-010", "domain": "ANIMISM_FUNDAMENTALS", "title": "Original soul-body dualism mirrors conscious-unconscious division", "source": source, "text_evidence": "Original soul-body dualism mirrors conscious-unconscious division"},
    {"id": "ANIM-011", "position_id": "ANIM-011", "domain": "ANIMISM_FUNDAMENTALS", "title": "Demon conceptions derived from ambivalent relation to dead", "source": source, "text_evidence": "Demon conceptions derived from ambivalent relation to dead"},
    {"id": "ANIM-012", "position_id": "ANIM-012", "domain": "ANIMISM_FUNDAMENTALS", "title": "Ancestral reverence evolves from initial demonic fear", "source": source, "text_evidence": "Ancestral reverence evolves from initial demonic fear"},
])

# MAGIC_THEORY (15)
new_positions.extend([
    {"id": "MAGI-001", "position_id": "MAGI-001", "domain": "MAGIC_THEORY", "title": "Magic is strategy/technique of animistic system", "source": source, "text_evidence": "Magic is strategy/technique of animistic system"},
    {"id": "MAGI-002", "position_id": "MAGI-002", "domain": "MAGIC_THEORY", "title": "Magic aims to master men, animals, things and their spirits", "source": source, "text_evidence": "Magic aims to master men, animals, things and their spirits"},
    {"id": "MAGI-003", "position_id": "MAGI-003", "domain": "MAGIC_THEORY", "title": "Imitative magic based on principle of similarity", "source": source, "text_evidence": "Imitative magic based on principle of similarity"},
    {"id": "MAGI-004", "position_id": "MAGI-004", "domain": "MAGIC_THEORY", "title": "Contagious magic based on principle of contiguity/association", "source": source, "text_evidence": "Contagious magic based on principle of contiguity/association"},
    {"id": "MAGI-005", "position_id": "MAGI-005", "domain": "MAGIC_THEORY", "title": "Magic mistakes ideal connection for real connection", "source": source, "text_evidence": "Magic mistakes ideal connection for real connection"},
    {"id": "MAGI-006", "position_id": "MAGI-006", "domain": "MAGIC_THEORY", "title": "Association of ideas (similarity and contiguity) governs magic", "source": source, "text_evidence": "Association of ideas (similarity and contiguity) governs magic"},
    {"id": "MAGI-007", "position_id": "MAGI-007", "domain": "MAGIC_THEORY", "title": "Primitive man transfers psychological laws to natural world", "source": source, "text_evidence": "Primitive man transfers psychological laws to natural world"},
    {"id": "MAGI-008", "position_id": "MAGI-008", "domain": "MAGIC_THEORY", "title": "Magic action represents motor hallucination of wish fulfillment", "source": source, "text_evidence": "Magic action represents motor hallucination of wish fulfillment"},
    {"id": "MAGI-009", "position_id": "MAGI-009", "domain": "MAGIC_THEORY", "title": "Play and imitative representation satisfy wishes for primitive man", "source": source, "text_evidence": "Play and imitative representation satisfy wishes for primitive man"},
    {"id": "MAGI-010", "position_id": "MAGI-010", "domain": "MAGIC_THEORY", "title": "Magic assumes excessive valuation of psychic acts and thoughts", "source": source, "text_evidence": "Magic assumes excessive valuation of psychic acts and thoughts"},
    {"id": "MAGI-011", "position_id": "MAGI-011", "domain": "MAGIC_THEORY", "title": "Objects overshadowed by ideas representing them in magic thinking", "source": source, "text_evidence": "Objects overshadowed by ideas representing them in magic thinking"},
    {"id": "MAGI-012", "position_id": "MAGI-012", "domain": "MAGIC_THEORY", "title": "Words and names treated as possessing power over things", "source": source, "text_evidence": "Words and names treated as possessing power over things"},
    {"id": "MAGI-013", "position_id": "MAGI-013", "domain": "MAGIC_THEORY", "title": "Telepathy and action-at-distance assumed as self-evident", "source": source, "text_evidence": "Telepathy and action-at-distance assumed as self-evident"},
    {"id": "MAGI-014", "position_id": "MAGI-014", "domain": "MAGIC_THEORY", "title": "Magic precedes and is older than spirit animism", "source": source, "text_evidence": "Magic precedes and is older than spirit animism"},
    {"id": "MAGI-015", "position_id": "MAGI-015", "domain": "MAGIC_THEORY", "title": "Magic demonstrates practical need to master world not mere speculation", "source": source, "text_evidence": "Magic demonstrates practical need to master world not mere speculation"},
])

# OMNIPOTENCE_OF_THOUGHT (14)
new_positions.extend([
    {"id": "OMNI-001", "position_id": "OMNI-001", "domain": "OMNIPOTENCE_OF_THOUGHT", "title": "Omnipotence of thought is primitive belief in mind's power over reality", "source": source, "text_evidence": "Omnipotence of thought is primitive belief in mind's power over reality"},
    {"id": "OMNI-002", "position_id": "OMNI-002", "domain": "OMNIPOTENCE_OF_THOUGHT", "title": "Thought and wish given same value as accomplished deed", "source": source, "text_evidence": "Thought and wish given same value as accomplished deed"},
    {"id": "OMNI-003", "position_id": "OMNI-003", "domain": "OMNIPOTENCE_OF_THOUGHT", "title": "Compulsion neurotics preserve omnipotence of thought belief", "source": source, "text_evidence": "Compulsion neurotics preserve omnipotence of thought belief"},
    {"id": "OMNI-004", "position_id": "OMNI-004", "domain": "OMNIPOTENCE_OF_THOUGHT", "title": "Neurotics react to thoughts with same seriousness as to realities", "source": source, "text_evidence": "Neurotics react to thoughts with same seriousness as to realities"},
    {"id": "OMNI-005", "position_id": "OMNI-005", "domain": "OMNIPOTENCE_OF_THOUGHT", "title": "Fear of thought's realization creates superstitious behavior", "source": source, "text_evidence": "Fear of thought's realization creates superstitious behavior"},
    {"id": "OMNI-006", "position_id": "OMNI-006", "domain": "OMNIPOTENCE_OF_THOUGHT", "title": "Unconscious processes retain omnipotence more than conscious ones", "source": source, "text_evidence": "Unconscious processes retain omnipotence more than conscious ones"},
    {"id": "OMNI-007", "position_id": "OMNI-007", "domain": "OMNIPOTENCE_OF_THOUGHT", "title": "Narcistic phase characterized by thought omnipotence belief", "source": source, "text_evidence": "Narcistic phase characterized by thought omnipotence belief"},
    {"id": "OMNI-008", "position_id": "OMNI-008", "domain": "OMNIPOTENCE_OF_THOUGHT", "title": "Animistic phase corresponds to narcism in individual development", "source": source, "text_evidence": "Animistic phase corresponds to narcism in individual development"},
    {"id": "OMNI-009", "position_id": "OMNI-009", "domain": "OMNIPOTENCE_OF_THOUGHT", "title": "Religious phase corresponds to object-finding/parental dependence", "source": source, "text_evidence": "Religious phase corresponds to object-finding/parental dependence"},
    {"id": "OMNI-010", "position_id": "OMNI-010", "domain": "OMNIPOTENCE_OF_THOUGHT", "title": "Scientific phase corresponds to individual's mature reality adaptation", "source": source, "text_evidence": "Scientific phase corresponds to individual's mature reality adaptation"},
    {"id": "OMNI-011", "position_id": "OMNI-011", "domain": "OMNIPOTENCE_OF_THOUGHT", "title": "High sexualization of thinking produces omnipotence belief", "source": source, "text_evidence": "High sexualization of thinking produces omnipotence belief"},
    {"id": "OMNI-012", "position_id": "OMNI-012", "domain": "OMNIPOTENCE_OF_THOUGHT", "title": "Art preserves omnipotence of thought in cultural life", "source": source, "text_evidence": "Art preserves omnipotence of thought in cultural life"},
    {"id": "OMNI-013", "position_id": "OMNI-013", "domain": "OMNIPOTENCE_OF_THOUGHT", "title": "Magic thinking demonstrates wish's power through motor expression", "source": source, "text_evidence": "Magic thinking demonstrates wish's power through motor expression"},
    {"id": "OMNI-014", "position_id": "OMNI-014", "domain": "OMNIPOTENCE_OF_THOUGHT", "title": "Primitive man's thought has full value of deed not mere intention", "source": source, "text_evidence": "Primitive man's thought has full value of deed not mere intention"},
])

# PROJECTION_MECHANISM (9)
new_positions.extend([
    {"id": "PROJ-001", "position_id": "PROJ-001", "domain": "PROJECTION_MECHANISM", "title": "Projection is displacement of inner perceptions to outer world", "source": source, "text_evidence": "Projection is displacement of inner perceptions to outer world"},
    {"id": "PROJ-002", "position_id": "PROJ-002", "domain": "PROJECTION_MECHANISM", "title": "Hostile impulses projected onto external objects/persons", "source": source, "text_evidence": "Hostile impulses projected onto external objects/persons"},
    {"id": "PROJ-003", "position_id": "PROJ-003", "domain": "PROJECTION_MECHANISM", "title": "Projection resolves ambivalent emotional conflicts", "source": source, "text_evidence": "Projection resolves ambivalent emotional conflicts"},
    {"id": "PROJ-004", "position_id": "PROJ-004", "domain": "PROJECTION_MECHANISM", "title": "Spirit world created through projection of psychic processes", "source": source, "text_evidence": "Spirit world created through projection of psychic processes"},
    {"id": "PROJ-005", "position_id": "PROJ-005", "domain": "PROJECTION_MECHANISM", "title": "Perception and memory coexistence basis of soul projection", "source": source, "text_evidence": "Perception and memory coexistence basis of soul projection"},
    {"id": "PROJ-006", "position_id": "PROJ-006", "domain": "PROJECTION_MECHANISM", "title": "Primitive attention directed outward not inward facilitates projection", "source": source, "text_evidence": "Primitive attention directed outward not inward facilitates projection"},
    {"id": "PROJ-007", "position_id": "PROJ-007", "domain": "PROJECTION_MECHANISM", "title": "Demonic attributions represent projected hostile impulses", "source": source, "text_evidence": "Demonic attributions represent projected hostile impulses"},
    {"id": "PROJ-008", "position_id": "PROJ-008", "domain": "PROJECTION_MECHANISM", "title": "Projection permits expression of forbidden impulses as external threat", "source": source, "text_evidence": "Projection permits expression of forbidden impulses as external threat"},
    {"id": "PROJ-009", "position_id": "PROJ-009", "domain": "PROJECTION_MECHANISM", "title": "System formation (worldview) uses projection and secondary elaboration", "source": source, "text_evidence": "System formation (worldview) uses projection and secondary elaboration"},
])

# SACRIFICE_THEORY (17)
new_positions.extend([
    {"id": "SACR-001", "position_id": "SACR-001", "domain": "SACRIFICE_THEORY", "title": "Original sacrifice was social fellowship meal between deity and worshippers", "source": source, "text_evidence": "Original sacrifice was social fellowship meal between deity and worshippers"},
    {"id": "SACR-002", "position_id": "SACR-002", "domain": "SACRIFICE_THEORY", "title": "God and humans partake of same sacrificial flesh and blood", "source": source, "text_evidence": "God and humans partake of same sacrificial flesh and blood"},
    {"id": "SACR-003", "position_id": "SACR-003", "domain": "SACRIFICE_THEORY", "title": "Sacrificial feast establishes holy bond among participants", "source": source, "text_evidence": "Sacrificial feast establishes holy bond among participants"},
    {"id": "SACR-004", "position_id": "SACR-004", "domain": "SACRIFICE_THEORY", "title": "Eating together creates and confirms social community obligations", "source": source, "text_evidence": "Eating together creates and confirms social community obligations"},
    {"id": "SACR-005", "position_id": "SACR-005", "domain": "SACRIFICE_THEORY", "title": "Kinship originally conceived as sharing common bodily substance", "source": source, "text_evidence": "Kinship originally conceived as sharing common bodily substance"},
    {"id": "SACR-006", "position_id": "SACR-006", "domain": "SACRIFICE_THEORY", "title": "Sacrificial animal originally identical with totem animal", "source": source, "text_evidence": "Sacrificial animal originally identical with totem animal"},
    {"id": "SACR-007", "position_id": "SACR-007", "domain": "SACRIFICE_THEORY", "title": "Totem animal treated as member of kin in sacrificial context", "source": source, "text_evidence": "Totem animal treated as member of kin in sacrificial context"},
    {"id": "SACR-008", "position_id": "SACR-008", "domain": "SACRIFICE_THEORY", "title": "Killing totem animal required whole clan's consent and participation", "source": source, "text_evidence": "Killing totem animal required whole clan's consent and participation"},
    {"id": "SACR-009", "position_id": "SACR-009", "domain": "SACRIFICE_THEORY", "title": "Animal sacrifice preceded development of agriculture and pastoralism", "source": source, "text_evidence": "Animal sacrifice preceded development of agriculture and pastoralism"},
    {"id": "SACR-010", "position_id": "SACR-010", "domain": "SACRIFICE_THEORY", "title": "Holy animal could only be killed on solemn communal occasions", "source": source, "text_evidence": "Holy animal could only be killed on solemn communal occasions"},
    {"id": "SACR-011", "position_id": "SACR-011", "domain": "SACRIFICE_THEORY", "title": "Sacrificial eating conveys properties of consumed being to eater", "source": source, "text_evidence": "Sacrificial eating conveys properties of consumed being to eater"},
    {"id": "SACR-012", "position_id": "SACR-012", "domain": "SACRIFICE_THEORY", "title": "Totem feast involves ceremonial killing and raw consumption", "source": source, "text_evidence": "Totem feast involves ceremonial killing and raw consumption"},
    {"id": "SACR-013", "position_id": "SACR-013", "domain": "SACRIFICE_THEORY", "title": "Death of sacrificial animal bewailed and mourned compulsively", "source": source, "text_evidence": "Death of sacrificial animal bewailed and mourned compulsively"},
    {"id": "SACR-014", "position_id": "SACR-014", "domain": "SACRIFICE_THEORY", "title": "Holiday excess follows sacrifice through release of prohibitions", "source": source, "text_evidence": "Holiday excess follows sacrifice through release of prohibitions"},
    {"id": "SACR-015", "position_id": "SACR-015", "domain": "SACRIFICE_THEORY", "title": "Sacramental meaning of sacrifice more primitive than gift theory", "source": source, "text_evidence": "Sacramental meaning of sacrifice more primitive than gift theory"},
    {"id": "SACR-016", "position_id": "SACR-016", "domain": "SACRIFICE_THEORY", "title": "Blood bonds require periodic renewal through common meals", "source": source, "text_evidence": "Blood bonds require periodic renewal through common meals"},
    {"id": "SACR-017", "position_id": "SACR-017", "domain": "SACRIFICE_THEORY", "title": "Sacrifice later evolves from communion to offering to deity", "source": source, "text_evidence": "Sacrifice later evolves from communion to offering to deity"},
])

# PRIMAL_HORDE_THEORY (18)
new_positions.extend([
    {"id": "PRIM-001", "position_id": "PRIM-001", "domain": "PRIMAL_HORDE_THEORY", "title": "Primal horde consisted of violent jealous father and expelled sons", "source": source, "text_evidence": "Primal horde consisted of violent jealous father and expelled sons"},
    {"id": "PRIM-002", "position_id": "PRIM-002", "domain": "PRIMAL_HORDE_THEORY", "title": "Father monopolized all females and drove away maturing sons", "source": source, "text_evidence": "Father monopolized all females and drove away maturing sons"},
    {"id": "PRIM-003", "position_id": "PRIM-003", "domain": "PRIMAL_HORDE_THEORY", "title": "Expelled brothers eventually banded together and killed father", "source": source, "text_evidence": "Expelled brothers eventually banded together and killed father"},
    {"id": "PRIM-004", "position_id": "PRIM-004", "domain": "PRIMAL_HORDE_THEORY", "title": "Brothers devoured father's body in cannibalistic feast", "source": source, "text_evidence": "Brothers devoured father's body in cannibalistic feast"},
    {"id": "PRIM-005", "position_id": "PRIM-005", "domain": "PRIMAL_HORDE_THEORY", "title": "Parricide and consumption accomplished identification with father", "source": source, "text_evidence": "Parricide and consumption accomplished identification with father"},
    {"id": "PRIM-006", "position_id": "PRIM-006", "domain": "PRIMAL_HORDE_THEORY", "title": "Each son acquired part of father's strength through incorporation", "source": source, "text_evidence": "Each son acquired part of father's strength through incorporation"},
    {"id": "PRIM-007", "position_id": "PRIM-007", "domain": "PRIMAL_HORDE_THEORY", "title": "Brothers' ambivalence created remorse after satisfying hatred", "source": source, "text_evidence": "Brothers' ambivalence created remorse after satisfying hatred"},
    {"id": "PRIM-008", "position_id": "PRIM-008", "domain": "PRIMAL_HORDE_THEORY", "title": "Sense of guilt emerged from subsequent obedience to father", "source": source, "text_evidence": "Sense of guilt emerged from subsequent obedience to father"},
    {"id": "PRIM-009", "position_id": "PRIM-009", "domain": "PRIMAL_HORDE_THEORY", "title": "Dead father became stronger than living one had been", "source": source, "text_evidence": "Dead father became stronger than living one had been"},
    {"id": "PRIM-010", "position_id": "PRIM-010", "domain": "PRIMAL_HORDE_THEORY", "title": "Two fundamental taboos created from son's guilt correspond to Oedipus wishes", "source": source, "text_evidence": "Two fundamental taboos created from son's guilt correspond to Oedipus wishes"},
    {"id": "PRIM-011", "position_id": "PRIM-011", "domain": "PRIMAL_HORDE_THEORY", "title": "Prohibition against killing totem substitutes for murdered father", "source": source, "text_evidence": "Prohibition against killing totem substitutes for murdered father"},
    {"id": "PRIM-012", "position_id": "PRIM-012", "domain": "PRIMAL_HORDE_THEORY", "title": "Incest prohibition renounced fruits of parricide deed", "source": source, "text_evidence": "Incest prohibition renounced fruits of parricide deed"},
    {"id": "PRIM-013", "position_id": "PRIM-013", "domain": "PRIMAL_HORDE_THEORY", "title": "Exogamy prevents fraternal conflict over women", "source": source, "text_evidence": "Exogamy prevents fraternal conflict over women"},
    {"id": "PRIM-014", "position_id": "PRIM-014", "domain": "PRIMAL_HORDE_THEORY", "title": "Brother clan replaces father horde as social organization", "source": source, "text_evidence": "Brother clan replaces father horde as social organization"},
    {"id": "PRIM-015", "position_id": "PRIM-015", "domain": "PRIMAL_HORDE_THEORY", "title": "Social solidarity based on shared guilt for parricide", "source": source, "text_evidence": "Social solidarity based on shared guilt for parricide"},
    {"id": "PRIM-016", "position_id": "PRIM-016", "domain": "PRIMAL_HORDE_THEORY", "title": "Totem system represents reconciliation attempt with father", "source": source, "text_evidence": "Totem system represents reconciliation attempt with father"},
    {"id": "PRIM-017", "position_id": "PRIM-017", "domain": "PRIMAL_HORDE_THEORY", "title": "Father substitute (totem) granted protection in exchange for honor", "source": source, "text_evidence": "Father substitute (totem) granted protection in exchange for honor"},
    {"id": "PRIM-018", "position_id": "PRIM-018", "domain": "PRIMAL_HORDE_THEORY", "title": "Totemic religion issues from sons' sense of guilt", "source": source, "text_evidence": "Totemic religion issues from sons' sense of guilt"},
])

# OEDIPUS_COMPLEX (13)
new_positions.extend([
    {"id": "OEDI-001", "position_id": "OEDI-001", "domain": "OEDIPUS_COMPLEX", "title": "Child's first object selection incestuous toward mother", "source": source, "text_evidence": "Child's first object selection incestuous toward mother"},
    {"id": "OEDI-002", "position_id": "OEDI-002", "domain": "OEDIPUS_COMPLEX", "title": "Male child identifies father as rival for mother's affection", "source": source, "text_evidence": "Male child identifies father as rival for mother's affection"},
    {"id": "OEDI-003", "position_id": "OEDI-003", "domain": "OEDIPUS_COMPLEX", "title": "Boy harbors death wishes toward father", "source": source, "text_evidence": "Boy harbors death wishes toward father"},
    {"id": "OEDI-004", "position_id": "OEDI-004", "domain": "OEDIPUS_COMPLEX", "title": "Oedipus complex is nuclear complex of neuroses", "source": source, "text_evidence": "Oedipus complex is nuclear complex of neuroses"},
    {"id": "OEDI-005", "position_id": "OEDI-005", "domain": "OEDIPUS_COMPLEX", "title": "Totem prohibitions correspond to repressed Oedipus wishes", "source": source, "text_evidence": "Totem prohibitions correspond to repressed Oedipus wishes"},
    {"id": "OEDI-006", "position_id": "OEDI-006", "domain": "OEDIPUS_COMPLEX", "title": "Animal phobia in children displaces father-fear onto animal", "source": source, "text_evidence": "Animal phobia in children displaces father-fear onto animal"},
    {"id": "OEDI-007", "position_id": "OEDI-007", "domain": "OEDIPUS_COMPLEX", "title": "Feared animal represents father substitute in child's psyche", "source": source, "text_evidence": "Feared animal represents father substitute in child's psyche"},
    {"id": "OEDI-008", "position_id": "OEDI-008", "domain": "OEDIPUS_COMPLEX", "title": "Child's ambivalence toward father transferred to totem animal", "source": source, "text_evidence": "Child's ambivalence toward father transferred to totem animal"},
    {"id": "OEDI-009", "position_id": "OEDI-009", "domain": "OEDIPUS_COMPLEX", "title": "Identification with totem animal reflects father identification", "source": source, "text_evidence": "Identification with totem animal reflects father identification"},
    {"id": "OEDI-010", "position_id": "OEDI-010", "domain": "OEDIPUS_COMPLEX", "title": "Castration fear connected to father as threatening authority", "source": source, "text_evidence": "Castration fear connected to father as threatening authority"},
    {"id": "OEDI-011", "position_id": "OEDI-011", "domain": "OEDIPUS_COMPLEX", "title": "Animal phobia and totemism structurally identical", "source": source, "text_evidence": "Animal phobia and totemism structurally identical"},
    {"id": "OEDI-012", "position_id": "OEDI-012", "domain": "OEDIPUS_COMPLEX", "title": "Religion, morality, society, and art originate in Oedipus complex", "source": source, "text_evidence": "Religion, morality, society, and art originate in Oedipus complex"},
    {"id": "OEDI-013", "position_id": "OEDI-013", "domain": "OEDIPUS_COMPLEX", "title": "Father complex determines ambivalence in all authority relations", "source": source, "text_evidence": "Father complex determines ambivalence in all authority relations"},
])

# RELIGION_EVOLUTION (16)
new_positions.extend([
    {"id": "RELI-001", "position_id": "RELI-001", "domain": "RELIGION_EVOLUTION", "title": "Religion originates in remorse for primal parricide", "source": source, "text_evidence": "Religion originates in remorse for primal parricide"},
    {"id": "RELI-002", "position_id": "RELI-002", "domain": "RELIGION_EVOLUTION", "title": "Father substitute (totem) eventually regains human form as god", "source": source, "text_evidence": "Father substitute (totem) eventually regains human form as god"},
    {"id": "RELI-003", "position_id": "RELI-003", "domain": "RELIGION_EVOLUTION", "title": "God represents exalted and perfected father image", "source": source, "text_evidence": "God represents exalted and perfected father image"},
    {"id": "RELI-004", "position_id": "RELI-004", "domain": "RELIGION_EVOLUTION", "title": "Religion of son succeeds religion of father", "source": source, "text_evidence": "Religion of son succeeds religion of father"},
    {"id": "RELI-005", "position_id": "RELI-005", "domain": "RELIGION_EVOLUTION", "title": "Personal relation to god dependent on relation to physical father", "source": source, "text_evidence": "Personal relation to god dependent on relation to physical father"},
    {"id": "RELI-006", "position_id": "RELI-006", "domain": "RELIGION_EVOLUTION", "title": "God called father because modeled after father", "source": source, "text_evidence": "God called father because modeled after father"},
    {"id": "RELI-007", "position_id": "RELI-007", "domain": "RELIGION_EVOLUTION", "title": "Maternal deities historically preceded paternal deities", "source": source, "text_evidence": "Maternal deities historically preceded paternal deities"},
    {"id": "RELI-008", "position_id": "RELI-008", "domain": "RELIGION_EVOLUTION", "title": "Patriarchal society restored through religious father gods", "source": source, "text_evidence": "Patriarchal society restored through religious father gods"},
    {"id": "RELI-009", "position_id": "RELI-009", "domain": "RELIGION_EVOLUTION", "title": "Religious development shows increasing sons' defiance against father", "source": source, "text_evidence": "Religious development shows increasing sons' defiance against father"},
    {"id": "RELI-010", "position_id": "RELI-010", "domain": "RELIGION_EVOLUTION", "title": "Youthful dying gods (Attis, Adonis, Tammuz) represent son figures", "source": source, "text_evidence": "Youthful dying gods (Attis, Adonis, Tammuz) represent son figures"},
    {"id": "RELI-011", "position_id": "RELI-011", "domain": "RELIGION_EVOLUTION", "title": "Christianity achieves fullest expiation through son's self-sacrifice", "source": source, "text_evidence": "Christianity achieves fullest expiation through son's self-sacrifice"},
    {"id": "RELI-012", "position_id": "RELI-012", "domain": "RELIGION_EVOLUTION", "title": "Christ's sacrifice redeems mankind from original sin of parricide", "source": source, "text_evidence": "Christ's sacrifice redeems mankind from original sin of parricide"},
    {"id": "RELI-013", "position_id": "RELI-013", "domain": "RELIGION_EVOLUTION", "title": "Son becomes god beside/in place of father through sacrifice", "source": source, "text_evidence": "Son becomes god beside/in place of father through sacrifice"},
    {"id": "RELI-014", "position_id": "RELI-014", "domain": "RELIGION_EVOLUTION", "title": "Christian communion repeats and commemorates primal crime", "source": source, "text_evidence": "Christian communion repeats and commemorates primal crime"},
    {"id": "RELI-015", "position_id": "RELI-015", "domain": "RELIGION_EVOLUTION", "title": "Eucharist represents new setting aside of father", "source": source, "text_evidence": "Eucharist represents new setting aside of father"},
    {"id": "RELI-016", "position_id": "RELI-016", "domain": "RELIGION_EVOLUTION", "title": "Religious ambivalence maintains both expiation and defiance", "source": source, "text_evidence": "Religious ambivalence maintains both expiation and defiance"},
])

# CONSCIENCE_FORMATION (8)
new_positions.extend([
    {"id": "CONS-001", "position_id": "CONS-001", "domain": "CONSCIENCE_FORMATION", "title": "Conscience is inner perception of objections to wish impulses", "source": source, "text_evidence": "Conscience is inner perception of objections to wish impulses"},
    {"id": "CONS-002", "position_id": "CONS-002", "domain": "CONSCIENCE_FORMATION", "title": "Taboo conscience oldest form of conscience phenomenon", "source": source, "text_evidence": "Taboo conscience oldest form of conscience phenomenon"},
    {"id": "CONS-003", "position_id": "CONS-003", "domain": "CONSCIENCE_FORMATION", "title": "Guilty conscience arises without dependence on external factors", "source": source, "text_evidence": "Guilty conscience arises without dependence on external factors"},
    {"id": "CONS-004", "position_id": "CONS-004", "domain": "CONSCIENCE_FORMATION", "title": "Conscience originates from ambivalent emotional attitude", "source": source, "text_evidence": "Conscience originates from ambivalent emotional attitude"},
    {"id": "CONS-005", "position_id": "CONS-005", "domain": "CONSCIENCE_FORMATION", "title": "One component of ambivalence remains unconscious creating conscience", "source": source, "text_evidence": "One component of ambivalence remains unconscious creating conscience"},
    {"id": "CONS-006", "position_id": "CONS-006", "domain": "CONSCIENCE_FORMATION", "title": "Repressed hostility forms basis for sense of guilt", "source": source, "text_evidence": "Repressed hostility forms basis for sense of guilt"},
    {"id": "CONS-007", "position_id": "CONS-007", "domain": "CONSCIENCE_FORMATION", "title": "Conscience contains anxiety character pointing to unconscious sources", "source": source, "text_evidence": "Conscience contains anxiety character pointing to unconscious sources"},
    {"id": "CONS-008", "position_id": "CONS-008", "domain": "CONSCIENCE_FORMATION", "title": "Fear and anxiety in conscience reflect unknown unconscious motivation", "source": source, "text_evidence": "Fear and anxiety in conscience reflect unknown unconscious motivation"},
])

# SOCIAL_ORGANIZATION (11)
new_positions.extend([
    {"id": "SOCI-001", "position_id": "SOCI-001", "domain": "SOCIAL_ORGANIZATION", "title": "Brother clan created first social organization after parricide", "source": source, "text_evidence": "Brother clan created first social organization after parricide"},
    {"id": "SOCI-002", "position_id": "SOCI-002", "domain": "SOCIAL_ORGANIZATION", "title": "Social obligations originate in renunciation of father's privileges", "source": source, "text_evidence": "Social obligations originate in renunciation of father's privileges"},
    {"id": "SOCI-003", "position_id": "SOCI-003", "domain": "SOCIAL_ORGANIZATION", "title": "Blood solidarity replaces paternal domination", "source": source, "text_evidence": "Blood solidarity replaces paternal domination"},
    {"id": "SOCI-004", "position_id": "SOCI-004", "domain": "SOCIAL_ORGANIZATION", "title": "Prohibition against fratricide extends earlier taboos", "source": source, "text_evidence": "Prohibition against fratricide extends earlier taboos"},
    {"id": "SOCI-005", "position_id": "SOCI-005", "domain": "SOCIAL_ORGANIZATION", "title": "Society based on complicity in common crime", "source": source, "text_evidence": "Society based on complicity in common crime"},
    {"id": "SOCI-006", "position_id": "SOCI-006", "domain": "SOCIAL_ORGANIZATION", "title": "Morality based on necessities and expiation demands", "source": source, "text_evidence": "Morality based on necessities and expiation demands"},
    {"id": "SOCI-007", "position_id": "SOCI-007", "domain": "SOCIAL_ORGANIZATION", "title": "Matriarchy preceded restored patriarchal systems", "source": source, "text_evidence": "Matriarchy preceded restored patriarchal systems"},
    {"id": "SOCI-008", "position_id": "SOCI-008", "domain": "SOCIAL_ORGANIZATION", "title": "Democratic equality among brothers original social principle", "source": source, "text_evidence": "Democratic equality among brothers original social principle"},
    {"id": "SOCI-009", "position_id": "SOCI-009", "domain": "SOCIAL_ORGANIZATION", "title": "Totem clan represents reconstruction after primal horde dissolution", "source": source, "text_evidence": "Totem clan represents reconstruction after primal horde dissolution"},
    {"id": "SOCI-010", "position_id": "SOCI-010", "domain": "SOCIAL_ORGANIZATION", "title": "Exogamous restrictions ensure peaceful coexistence among brothers", "source": source, "text_evidence": "Exogamous restrictions ensure peaceful coexistence among brothers"},
    {"id": "SOCI-011", "position_id": "SOCI-011", "domain": "SOCIAL_ORGANIZATION", "title": "Cultural institutions preserve memory of primal deed", "source": source, "text_evidence": "Cultural institutions preserve memory of primal deed"},
])

# TRAGEDY_THEORY (7)
new_positions.extend([
    {"id": "TRAG-001", "position_id": "TRAG-001", "domain": "TRAGEDY_THEORY", "title": "Greek tragedy originated in totem feast ceremonies", "source": source, "text_evidence": "Greek tragedy originated in totem feast ceremonies"},
    {"id": "TRAG-002", "position_id": "TRAG-002", "domain": "TRAGEDY_THEORY", "title": "Tragic hero represents primal father figure", "source": source, "text_evidence": "Tragic hero represents primal father figure"},
    {"id": "TRAG-003", "position_id": "TRAG-003", "domain": "TRAGEDY_THEORY", "title": "Chorus represents band of brothers", "source": source, "text_evidence": "Chorus represents band of brothers"},
    {"id": "TRAG-004", "position_id": "TRAG-004", "domain": "TRAGEDY_THEORY", "title": "Hero's suffering punishment for presumption against authority", "source": source, "text_evidence": "Hero's suffering punishment for presumption against authority"},
    {"id": "TRAG-005", "position_id": "TRAG-005", "domain": "TRAGEDY_THEORY", "title": "Tragic guilt displaces actual guilt of chorus onto hero", "source": source, "text_evidence": "Tragic guilt displaces actual guilt of chorus onto hero"},
    {"id": "TRAG-006", "position_id": "TRAG-006", "domain": "TRAGEDY_THEORY", "title": "Tragedy reverses historical reality through purposive distortion", "source": source, "text_evidence": "Tragedy reverses historical reality through purposive distortion"},
    {"id": "TRAG-007", "position_id": "TRAG-007", "domain": "TRAGEDY_THEORY", "title": "Suffering god Dionysos reflects totem animal sacrifice", "source": source, "text_evidence": "Suffering god Dionysos reflects totem animal sacrifice"},
])

# NEUROSIS_CULTURE_PARALLEL (10)
new_positions.extend([
    {"id": "NEUR-001", "position_id": "NEUR-001", "domain": "NEUROSIS_CULTURE_PARALLEL", "title": "Neuroses are asocial formations seeking private solutions", "source": source, "text_evidence": "Neuroses are asocial formations seeking private solutions"},
    {"id": "NEUR-002", "position_id": "NEUR-002", "domain": "NEUROSIS_CULTURE_PARALLEL", "title": "Neurotic symptoms caricature cultural creations", "source": source, "text_evidence": "Neurotic symptoms caricature cultural creations"},
    {"id": "NEUR-003", "position_id": "NEUR-003", "domain": "NEUROSIS_CULTURE_PARALLEL", "title": "Compulsion neurosis is caricature of religion", "source": source, "text_evidence": "Compulsion neurosis is caricature of religion"},
    {"id": "NEUR-004", "position_id": "NEUR-004", "domain": "NEUROSIS_CULTURE_PARALLEL", "title": "Hysteria is caricature of artistic creation", "source": source, "text_evidence": "Hysteria is caricature of artistic creation"},
    {"id": "NEUR-005", "position_id": "NEUR-005", "domain": "NEUROSIS_CULTURE_PARALLEL", "title": "Paranoia is caricature of philosophic system", "source": source, "text_evidence": "Paranoia is caricature of philosophic system"},
    {"id": "NEUR-006", "position_id": "NEUR-006", "domain": "NEUROSIS_CULTURE_PARALLEL", "title": "Cultural products rest on social impulses neuroses lack", "source": source, "text_evidence": "Cultural products rest on social impulses neuroses lack"},
    {"id": "NEUR-007", "position_id": "NEUR-007", "domain": "NEUROSIS_CULTURE_PARALLEL", "title": "Neurotic symptom represents failed adjustment to reality", "source": source, "text_evidence": "Neurotic symptom represents failed adjustment to reality"},
    {"id": "NEUR-008", "position_id": "NEUR-008", "domain": "NEUROSIS_CULTURE_PARALLEL", "title": "Neurotic withdrew from dissatisfying reality to fantasy world", "source": source, "text_evidence": "Neurotic withdrew from dissatisfying reality to fantasy world"},
    {"id": "NEUR-009", "position_id": "NEUR-009", "domain": "NEUROSIS_CULTURE_PARALLEL", "title": "Over-morality in neurotic results from childhood perverse phase", "source": source, "text_evidence": "Over-morality in neurotic results from childhood perverse phase"},
    {"id": "NEUR-010", "position_id": "NEUR-010", "domain": "NEUROSIS_CULTURE_PARALLEL", "title": "Psychic reality has full pathogenic value in neurosis", "source": source, "text_evidence": "Psychic reality has full pathogenic value in neurosis"},
])

# PHYLOGENETIC_INHERITANCE (9)
new_positions.extend([
    {"id": "PHYL-001", "position_id": "PHYL-001", "domain": "PHYLOGENETIC_INHERITANCE", "title": "Psychic continuity exists across generations beyond individual", "source": source, "text_evidence": "Psychic continuity exists across generations beyond individual"},
    {"id": "PHYL-002", "position_id": "PHYL-002", "domain": "PHYLOGENETIC_INHERITANCE", "title": "Mass psyche preserves emotional processes through time", "source": source, "text_evidence": "Mass psyche preserves emotional processes through time"},
    {"id": "PHYL-003", "position_id": "PHYL-003", "domain": "PHYLOGENETIC_INHERITANCE", "title": "Inheritance of psychic dispositions supplements tradition", "source": source, "text_evidence": "Inheritance of psychic dispositions supplements tradition"},
    {"id": "PHYL-004", "position_id": "PHYL-004", "domain": "PHYLOGENETIC_INHERITANCE", "title": "Unconscious understanding enables interpreting others' reactions", "source": source, "text_evidence": "Unconscious understanding enables interpreting others' reactions"},
    {"id": "PHYL-005", "position_id": "PHYL-005", "domain": "PHYLOGENETIC_INHERITANCE", "title": "Each generation deciphers previous generation's distortions", "source": source, "text_evidence": "Each generation deciphers previous generation's distortions"},
    {"id": "PHYL-006", "position_id": "PHYL-006", "domain": "PHYLOGENETIC_INHERITANCE", "title": "Sense of guilt for primal crime transmitted hereditarily", "source": source, "text_evidence": "Sense of guilt for primal crime transmitted hereditarily"},
    {"id": "PHYL-007", "position_id": "PHYL-007", "domain": "PHYLOGENETIC_INHERITANCE", "title": "Psychic traces remain despite attempts at forgetting", "source": source, "text_evidence": "Psychic traces remain despite attempts at forgetting"},
    {"id": "PHYL-008", "position_id": "PHYL-008", "domain": "PHYLOGENETIC_INHERITANCE", "title": "Symbolic systems (totemism) preserve historical memory", "source": source, "text_evidence": "Symbolic systems (totemism) preserve historical memory"},
    {"id": "PHYL-009", "position_id": "PHYL-009", "domain": "PHYLOGENETIC_INHERITANCE", "title": "Original deed retains psychological power across millennia", "source": source, "text_evidence": "Original deed retains psychological power across millennia"},
])

# NARCISSISM_THEORY (6)
new_positions.extend([
    {"id": "NARC-001", "position_id": "NARC-001", "domain": "NARCISSISM_THEORY", "title": "Narcistic stage intervenes between autoerotism and object-love", "source": source, "text_evidence": "Narcistic stage intervenes between autoerotism and object-love"},
    {"id": "NARC-002", "position_id": "NARC-002", "domain": "NARCISSISM_THEORY", "title": "In narcism ego becomes object of sexual impulses", "source": source, "text_evidence": "In narcism ego becomes object of sexual impulses"},
    {"id": "NARC-003", "position_id": "NARC-003", "domain": "NARCISSISM_THEORY", "title": "Sexual impulses combine into unity during narcistic phase", "source": source, "text_evidence": "Sexual impulses combine into unity during narcistic phase"},
    {"id": "NARC-004", "position_id": "NARC-004", "domain": "NARCISSISM_THEORY", "title": "High narcism characterized by thought overvaluation", "source": source, "text_evidence": "High narcism characterized by thought overvaluation"},
    {"id": "NARC-005", "position_id": "NARC-005", "domain": "NARCISSISM_THEORY", "title": "Primitive races remain in narcistic developmental stage", "source": source, "text_evidence": "Primitive races remain in narcistic developmental stage"},
    {"id": "NARC-006", "position_id": "NARC-006", "domain": "NARCISSISM_THEORY", "title": "Intellectual narcism produces omnipotence of thought belief", "source": source, "text_evidence": "Intellectual narcism produces omnipotence of thought belief"},
])

# SYMBOLISM (8)
new_positions.extend([
    {"id": "SYMB-001", "position_id": "SYMB-001", "domain": "SYMBOLISM", "title": "Totem animal symbolically represents father", "source": source, "text_evidence": "Totem animal symbolically represents father"},
    {"id": "SYMB-002", "position_id": "SYMB-002", "domain": "SYMBOLISM", "title": "Sacrificial animal stands for both god and father", "source": source, "text_evidence": "Sacrificial animal stands for both god and father"},
    {"id": "SYMB-003", "position_id": "SYMB-003", "domain": "SYMBOLISM", "title": "Father appears twice in sacrifice scene (as god and victim)", "source": source, "text_evidence": "Father appears twice in sacrifice scene (as god and victim)"},
    {"id": "SYMB-004", "position_id": "SYMB-004", "domain": "SYMBOLISM", "title": "Killing of sacred animal represents father's degradation and triumph", "source": source, "text_evidence": "Killing of sacred animal represents father's degradation and triumph"},
    {"id": "SYMB-005", "position_id": "SYMB-005", "domain": "SYMBOLISM", "title": "Names possess magical power over persons and things", "source": source, "text_evidence": "Names possess magical power over persons and things"},
    {"id": "SYMB-006", "position_id": "SYMB-006", "domain": "SYMBOLISM", "title": "Totemic identification expresses blood kinship symbolically", "source": source, "text_evidence": "Totemic identification expresses blood kinship symbolically"},
    {"id": "SYMB-007", "position_id": "SYMB-007", "domain": "SYMBOLISM", "title": "Ceremonial customs symbolically preserve historical events", "source": source, "text_evidence": "Ceremonial customs symbolically preserve historical events"},
    {"id": "SYMB-008", "position_id": "SYMB-008", "domain": "SYMBOLISM", "title": "Dream-like distortion operates in myth and religious symbolism", "source": source, "text_evidence": "Dream-like distortion operates in myth and religious symbolism"},
])

# WISH_FULFILLMENT (7)
new_positions.extend([
    {"id": "WISH-001", "position_id": "WISH-001", "domain": "WISH_FULFILLMENT", "title": "Myths represent collective wish phantasies projected into past", "source": source, "text_evidence": "Myths represent collective wish phantasies projected into past"},
    {"id": "WISH-002", "position_id": "WISH-002", "domain": "WISH_FULFILLMENT", "title": "Golden age myths reflect wish for freedom from restrictions", "source": source, "text_evidence": "Golden age myths reflect wish for freedom from restrictions"},
    {"id": "WISH-003", "position_id": "WISH-003", "domain": "WISH_FULFILLMENT", "title": "Totem feast holiday gratifies forbidden wish impulses", "source": source, "text_evidence": "Totem feast holiday gratifies forbidden wish impulses"},
    {"id": "WISH-004", "position_id": "WISH-004", "domain": "WISH_FULFILLMENT", "title": "Son's wish to replace father preserved in religious evolution", "source": source, "text_evidence": "Son's wish to replace father preserved in religious evolution"},
    {"id": "WISH-005", "position_id": "WISH-005", "domain": "WISH_FULFILLMENT", "title": "Deification of hero fulfills wish for father's power", "source": source, "text_evidence": "Deification of hero fulfills wish for father's power"},
    {"id": "WISH-006", "position_id": "WISH-006", "domain": "WISH_FULFILLMENT", "title": "Religious ceremony commemorates wish fulfillment through deed repetition", "source": source, "text_evidence": "Religious ceremony commemorates wish fulfillment through deed repetition"},
    {"id": "WISH-007", "position_id": "WISH-007", "domain": "WISH_FULFILLMENT", "title": "Art permits wish fulfillment through illusion and magic", "source": source, "text_evidence": "Art permits wish fulfillment through illusion and magic"},
])

# TOTAL_FOR_TOTEM_AND_TABOO (0)
new_positions.extend([
])

# UPDATED_DATABASE_TOTAL (0)
new_positions.extend([
])

# Add all positions to database
data['positions'].extend(new_positions)

# Update WORK-006 entry
work_006 = {
    "work_id": "WORK-006",
    "title": "Totem and Taboo",
    "year": 1913,
    "position_count": len(new_positions)
}

if 'works' not in data:
    data['works'] = []
data['works'].append(work_006)

# Update metadata
data['metadata']['version'] = 'v6_TOTEM_TABOO_ADDED'
data['metadata']['total_positions'] = len(data['positions'])
data['metadata']['date_created'] = 'November 17, 2025'

# Save
with open('data/FREUD_DATABASE.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"✓ Successfully added {len(new_positions)} new positions!")
print(f"✓ New total: {data['metadata']['total_positions']} positions")
print(f"✓ New version: {data['metadata']['version']}")
