from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "pr_joint_submission_package"


TITLE = "AutoArchival: LLM-Guided Architecture Search for Vertical Mongolian-Chinese Historical Text Spotting"
SHORT_TITLE = "AutoArchival for Historical Text Spotting"
AUTHOR_LINE = "Lanying Liang [1], Yuefeng Liu [2], Jianjun Zhao [3]"
AFFILIATIONS = [
    "1 Archives, Inner Mongolia University of Science and Technology, Baotou 014010, Inner Mongolia, China",
    "2 School of Artificial Intelligence and Data Science (School of Cyber Security), Inner Mongolia University of Science and Technology, Baotou 014010, Inner Mongolia, China",
    "3 Faculty of Information Science and Electrical Engineering, Kyushu University, Fukuoka, Japan",
]
CORRESPONDING_AUTHOR = (
    "Corresponding author: Yuefeng Liu, liuyuefeng@imust.edu.cn, "
    "School of Artificial Intelligence and Data Science, Inner Mongolia University of Science and Technology, "
    "Baotou 014010, Inner Mongolia, China"
)
ADDITIONAL_EMAILS = ["Jianjun Zhao email: zhao@ait.kyushu-u.ac.jp"]
AUTHOR_BIOS = [
    "Lanying Liang is an Associate Research Librarian at the Archives of Inner Mongolia University of Science and Technology. Her research interests include historical document management and digitization.",
    "Yuefeng Liu is a Professor at the School of Artificial Intelligence and Data Science (School of Cyber Security), Inner Mongolia University of Science and Technology. His research interests include computer vision and deep learning.",
    "Jianjun Zhao is a Professor at the Faculty of Information Science and Electrical Engineering, Kyushu University. His research interests include software engineering, program analysis, and intelligent software systems.",
]
FUNDING_STATEMENT = (
    "This work was supported by the National Natural Science Foundation of China "
    "(Grant No. 62341604), the Science and Technology Project of Inner Mongolia "
    "Autonomous Region Archives Bureau (Grant No. 2022-36), the China Scholarship "
    "Council (Grant No. 202408150080), and the General Project of the 14th Five-Year "
    "Plan for Educational Science of Inner Mongolia Autonomous Region (Grant No. NGJGH2025013)."
)
CREDIT_STATEMENT = (
    "Lanying Liang: Conceptualization, Data Curation, Writing - Original Draft. "
    "Yuefeng Liu: Methodology, Software, Validation, Writing - Review & Editing, Supervision. "
    "Jianjun Zhao: Writing - Review & Editing, Supervision."
)
COMPETING_INTEREST_STATEMENT = (
    "The authors declare that they have no known competing financial interests or "
    "personal relationships that could have appeared to influence the work reported in this paper."
)
AI_DECLARATION = (
    "Generative AI technologies (Claude/Gemini) were used solely for manuscript formatting "
    "and grammatical polishing."
)
ACKNOWLEDGEMENTS = (
    "The authors would like to thank the Inner Mongolia Autonomous Region Archives Bureau for their support."
)
KEYWORDS = [
    "Historical document text spotting",
    "Large language models",
    "Neural architecture search",
    "Mongolian-Chinese archives",
    "Joint detection and OCR",
]


REFERENCES = [
    "[1] M. Alberti et al., “A labeled dataset for document layout analysis of historical handwritten databases,” in ICFHR, 2016.",
    "[2] Z. Zhong et al., “PubLayNet: largest dataset ever for document layout analysis,” in ICDAR, 2019.",
    "[3] A. Antonacopoulos et al., “ICDAR 2009 page segmentation competition,” in ICDAR, 2009.",
    "[4] K. Chen et al., “MMOCR: A comprehensive toolbox for text detection, recognition and understanding,” in ACM MM, 2021.",
    "[5] H. Zhang et al., “Mongolian handwritten word recognition based on CNN and RNN,” in ICDAR, 2017.",
    "[6] M. Wei et al., “Traditional Mongolian text detection in natural scenes,” in ICDAR, 2019.",
    "[7] B. Gatos et al., “Adaptive degraded document image binarization,” Pattern Recognition, 2006.",
    "[8] C. Tensmeyer et al., “Document image binarization with fully convolutional neural networks,” in ICDAR, 2017.",
    "[9] Q. Le et al., “Using deep learning for historical document analysis,” IJDAR, 2019.",
    "[10] M. Liao et al., “Real-time scene text detection with differentiable binarization,” in AAAI, 2020.",
    "[11] X. Zhou et al., “EAST: an efficient and accurate scene text detector,” in CVPR, 2017.",
    "[12] Y. Baek et al., “Character region awareness for text detection,” in CVPR, 2019.",
    "[13] W. Wang et al., “Shape robust text detection with progressive scale expansion network,” in CVPR, 2019.",
    "[14] Y. Zhu et al., “Fourier contour embedding for arbitrary-shaped text detection,” in CVPR, 2021.",
    "[15] Y. Liu et al., “FOTS: Fast oriented text spotting with a unified network,” in CVPR, 2018.",
    "[16] B. Zoph and Q. V. Le, “Neural architecture search with reinforcement learning,” in ICLR, 2017.",
    "[17] G. Ghiasi et al., “NAS-FPN: Learning scalable feature pyramid architecture for object detection,” in CVPR, 2019.",
    "[18] C. Liu et al., “Auto-DeepLab: Hierarchical neural architecture search for semantic image segmentation,” in CVPR, 2019.",
    "[19] P. Lyu et al., “Auto-text: Automatic neural architecture search for text detection,” in AAAI, 2021.",
    "[20] T. Brown et al., “Language models are few-shot learners,” NeurIPS, 2020.",
    "[21] J. Wei et al., “Chain-of-thought prompting elicits reasoning in large language models,” NeurIPS, 2022.",
    "[22] H. Cai et al., “ProxylessNAS: Direct neural architecture search on target task and hardware,” in ICLR, 2019.",
    "[23] M. Alberti et al., “Historical document layout analysis using convolutional neural networks,” in IAPR, 2017.",
    "[24] M. Li et al., “DocBank: A benchmark dataset for document layout analysis,” in COLING, 2020.",
    "[25] Y. Gao et al., “Offline handwritten traditional Mongolian word recognition with deep convolutional neural networks,” IJDAR, 2021.",
    "[26] S. Yuan et al., “A novel sequence-to-sequence model for traditional Mongolian text recognition,” Pattern Recognition Letters, 2021.",
    "[27] T. Zhao et al., “A robust and efficient approach for traditional Mongolian historical document analysis,” IEEE Access, 2022.",
    "[28] Z. Qiao et al., “SEED: Semantics enhanced encoder-decoder framework for scene text recognition,” in CVPR, 2020.",
    "[29] L. Neumann and M. Matas, “Real-time scene text localization and recognition,” in CVPR, 2012.",
    "[30] Z. Guo et al., “Single path one-shot neural architecture search with uniform sampling,” in ECCV, 2020.",
    "[31] J. Wang et al., “Deep TextSpotter: An end-to-end trainable scene text spotting system,” in ICCV, 2017.",
    "[32] Y. He et al., “AutoML: A survey of the state-of-the-art,” KBS, 2021.",
    "[33] H. Liu, K. Simonyan, and Y. Yang, “DARTS: Differentiable architecture search,” in ICLR, 2019.",
    "[34] H. Pham et al., “Efficient neural architecture search via parameter sharing,” in ICML, 2018.",
    "[35] C. Yang et al., “Large language models as optimizers,” in ICLR, 2024.",
    "[36] G. Wang et al., “Voyager: An open-ended embodied agent with large language models,” arXiv preprint, 2023.",
    "[37] S. Yao et al., “ReAct: Synergizing reasoning and acting in language models,” in ICLR, 2023.",
    "[38] N. Shinn et al., “Reflexion: language agents with verbal reinforcement learning,” NeurIPS, 2023.",
]


def add_page_number(paragraph):
    run = paragraph.add_run()
    fld_char1 = OxmlElement("w:fldChar")
    fld_char1.set(qn("w:fldCharType"), "begin")
    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = "PAGE"
    fld_char2 = OxmlElement("w:fldChar")
    fld_char2.set(qn("w:fldCharType"), "end")
    run._r.append(fld_char1)
    run._r.append(instr_text)
    run._r.append(fld_char2)


def configure_document(doc: Document):
    section = doc.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Times New Roman"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    normal.font.size = Pt(10)

    for style_name in ["Title", "Heading 1", "Heading 2", "Heading 3"]:
        style = styles[style_name]
        style.font.name = "Times New Roman"
        style._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")

    styles["Title"].font.size = Pt(14)
    styles["Heading 1"].font.size = Pt(12)
    styles["Heading 2"].font.size = Pt(11)
    styles["Heading 3"].font.size = Pt(10.5)

    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_page_number(p)


def add_body_paragraph(doc: Document, text: str):
    p = doc.add_paragraph(style="Normal")
    fmt = p.paragraph_format
    fmt.line_spacing = 1.5
    fmt.space_after = Pt(6)
    fmt.first_line_indent = Inches(0.25)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(text)
    return p


def add_caption(doc: Document, text: str):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fmt = p.paragraph_format
    fmt.line_spacing = 1.0
    fmt.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    run.font.size = Pt(8)
    run.italic = True
    return p


def add_placeholder_figure(doc: Document, label: str, caption: str):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fmt = p.paragraph_format
    fmt.line_spacing = 1.0
    fmt.space_after = Pt(2)
    run = p.add_run(f"[Insert {label} here: replace with final figure asset before submission]")
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    run.font.size = Pt(9)
    run.bold = True
    add_caption(doc, caption)


def add_table(doc: Document, title: str, headers, rows):
    add_caption(doc, title)
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    for i, header in enumerate(headers):
        hdr[i].text = header
    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = value
    doc.add_paragraph("")
    return table


def build_manuscript():
    doc = Document()
    configure_document(doc)

    title = doc.add_paragraph(style="Title")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.line_spacing = 1.0
    title.add_run(TITLE)

    note = doc.add_paragraph()
    note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    note_run = note.add_run(
        "Draft prepared for Pattern Recognition submission. Replace bracketed placeholders "
        "with verified experimental values and benchmark names before submission."
    )
    note_run.italic = True
    note_run.font.name = "Times New Roman"
    note_run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    note_run.font.size = Pt(9)

    kw = doc.add_paragraph()
    kw.paragraph_format.line_spacing = 1.5
    kw_run = kw.add_run("Keywords: " + ", ".join(KEYWORDS))
    kw_run.font.name = "Times New Roman"
    kw_run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    kw_run.font.size = Pt(10)

    doc.add_heading("Abstract", level=1)
    add_body_paragraph(
        doc,
        "Joint text detection and recognition in Mongolian-Chinese historical archives remains "
        "challenging because the target documents contain severe degradation, vertically elongated "
        "text instances, mixed script layouts, and limited annotated data. Existing end-to-end text "
        "spotting methods are largely optimized for natural scenes or horizontally arranged text, and "
        "their manually engineered architectures often transfer poorly to historical documents with "
        "strong directional structure. In this paper, we present AutoArchival, a budget-constrained "
        "LLM-guided code-level architecture search framework for historical document text spotting. "
        "Starting from a lightweight joint baseline, the framework iteratively mutates editable model "
        "regions that control feature extraction, region alignment, and sequence decoding, while "
        "keeping the training and evaluation pipeline fixed. Candidate architectures are accepted only "
        "when they improve a joint validation criterion under a strict resource budget. The resulting "
        "model is evaluated with end-to-end spotting as the primary metric, while detection and "
        "recognition sub-metrics are reported separately to explain the source of the gains. "
        "Experiments on [PUBLIC-BENCHMARK-1], [PUBLIC-BENCHMARK-2], and the Mongolian-Chinese "
        "Historical Archive Dataset (MCAD) show that AutoArchival improves the joint spotting score by "
        "[XX.X] points over the manually designed baseline while maintaining a compact parameter budget. "
        "These results indicate that budget-constrained LLM-guided architecture search is a practical "
        "way to adapt end-to-end spotting models to structurally specialized historical documents."
    )

    doc.add_heading("1. Introduction", level=1)
    intro_paragraphs = [
        "The digitization of historical archives is an important prerequisite for cultural heritage preservation, retrieval, and large-scale humanities research. In many practical collections, however, automatic understanding of archival pages remains difficult because the documents contain severe degradation, non-uniform layouts, and script-specific writing conventions. Mongolian-Chinese archival materials are particularly challenging because vertically arranged Mongolian text often coexists with Chinese characters, seals, marginal notes, and heavily corrupted backgrounds.",
        "Most existing scene text systems are designed either for text detection or for end-to-end text spotting in modern natural images. Although these methods have demonstrated strong performance on public benchmarks, they often assume horizontal or mildly rotated text, cleaner visual appearance, and more regular region geometry. As a result, manually designed architectures may not transfer well to historical pages containing elongated vertical text lines, broken strokes, bleed-through, faded ink, and mixed writing directions.",
        "Recent large language models have shown the ability to reason about code, propose implementation-level changes, and iteratively improve algorithmic systems from feedback. This creates an opportunity to move beyond traditional neural architecture search spaces defined by fixed cells or limited operation pools. Instead of asking human designers to repeatedly redesign the network for a highly specialized archival domain, we investigate whether a constrained language-model-driven search process can discover architectural patterns that jointly benefit text localization and transcription.",
        "In this work, we present AutoArchival, a budget-constrained LLM-guided architecture search framework for historical document text spotting. The framework begins with a lightweight joint baseline and allows a language model to modify only predefined architecture-related code regions, including directional receptive-field modules, alignment interfaces between detection and recognition, and lightweight context fusion blocks. Candidate architectures are evaluated under a fixed resource budget and selected using a joint validation criterion that emphasizes end-to-end spotting quality while retaining visibility into detection and recognition sub-performance.",
    ]
    for paragraph in intro_paragraphs:
        add_body_paragraph(doc, paragraph)

    contrib = doc.add_paragraph()
    contrib.paragraph_format.line_spacing = 1.5
    contrib.paragraph_format.space_after = Pt(6)
    contrib.add_run("The main contributions of this paper are as follows. ").bold = True
    items = [
        "We formulate Mongolian-Chinese historical archive analysis as a joint text detection and text spotting problem with end-to-end spotting as the primary evaluation view.",
        "We propose a budget-constrained LLM-guided code-level architecture search framework that modifies editable detector-recognizer components while keeping the training protocol fixed.",
        "We introduce a joint evaluation and reporting scheme that separates detection, recognition, and end-to-end spotting quality, enabling a consistent interpretation of the search outcome.",
        "We organize experiments on public text spotting benchmarks and MCAD to analyze effectiveness, efficiency, and qualitative behavior in degraded archival settings.",
    ]
    contrib.add_run(" ".join(f"({i + 1}) {item}" for i, item in enumerate(items)))

    doc.add_heading("2. Related Work", level=1)
    doc.add_heading("2.1 Historical document analysis", level=2)
    add_body_paragraph(
        doc,
        "Historical document analysis has progressed from page segmentation and binarization to richer tasks such as layout analysis, text detection, and handwriting recognition. Prior work has shown that degraded manuscripts and archival documents require stronger noise robustness and structural modeling than standard scene text benchmarks. However, most existing historical document studies focus on segmentation or recognition in narrowly defined settings rather than unified text spotting in vertically structured bilingual archives."
    )
    doc.add_heading("2.2 Scene text detection and text spotting", level=2)
    add_body_paragraph(
        doc,
        "Modern text spotting frameworks combine text localization and sequence decoding in a unified architecture, enabling end-to-end training and evaluation. Representative systems such as FOTS, Deep TextSpotter, and related encoder-decoder methods have established the value of coupling detection and recognition. Nevertheless, these methods are still primarily tuned for natural scenes and do not explicitly address the elongated, vertically dominant text geometry found in Mongolian-Chinese historical archives."
    )
    doc.add_heading("2.3 Neural architecture search for dense prediction", level=2)
    add_body_paragraph(
        doc,
        "Neural architecture search has produced strong models for classification, detection, and segmentation, but conventional NAS methods often rely on expensive search procedures and rigid search spaces. Dense prediction tasks are particularly costly because improvements depend on both local detail preservation and large-context reasoning. For historical document spotting, these limitations make exhaustive manual or automated search difficult to sustain."
    )
    doc.add_heading("2.4 LLMs for code-level optimization", level=2)
    add_body_paragraph(
        doc,
        "Large language models can now generate, inspect, and revise executable deep learning code from structured feedback. This capability enables a broader search paradigm in which architecture design is performed at the source-code level rather than inside a fixed operation graph. Our work extends this idea to end-to-end historical document text spotting under explicit resource constraints."
    )

    doc.add_heading("3. Proposed Method", level=1)
    method_sections = {
        "3.1 Problem definition": [
            "We formulate Mongolian-Chinese historical document analysis as a joint text detection and text spotting problem. Given an input document image x, the model predicts text regions and the corresponding transcription sequences for each detected instance. Let y_det denote the detection annotations and y_rec denote the transcription labels. The objective is to learn a unified mapping f(x; theta) -> (y_det, y_rec), where theta denotes the model parameters.",
            "This setting is more difficult than standard scene text spotting for three reasons. First, historical pages contain severe degradation, including bleed-through, stains, faded strokes, and structural damage. Second, vertically arranged Mongolian text creates long anisotropic regions that violate the horizontal bias of many modern text recognition pipelines. Third, mixed-script pages introduce interactions between localization and transcription that are sensitive to the quality of aligned regional features. These characteristics motivate a joint architecture in which the detector and recognizer are co-designed rather than optimized independently.",
        ],
        "3.2 Baseline joint architecture": [
            "AutoArchival starts from a lightweight end-to-end baseline containing a multi-scale visual encoder, a detection branch, a region-alignment module, and a recognition branch. The encoder uses a feature pyramid design to preserve both semantic context and stroke-level detail. The detection branch predicts text regions from fused multi-scale features, while the recognition branch extracts aligned regional features and decodes them into character sequences.",
            "To better support vertically elongated Mongolian text, the baseline introduces a vertical-aware sequence extraction mechanism that treats the dominant text direction as the primary decoding axis. The aligned feature map is transformed into a one-dimensional sequence representation and passed to a recurrent or sequence-modeling decoder supervised with a transcription loss. This baseline is intentionally compact so that subsequent gains can be attributed to the searched architectural changes rather than excessive manual complexity.",
        ],
        "3.3 Search space and editable components": [
            "The search framework operates at the code level but only within predefined editable regions. Rather than permitting unrestricted modifications to the entire training codebase, we constrain the language model to architecture-related components that influence joint spotting quality: convolutional feature blocks, feature-fusion modules, directional context modules, region-alignment layers, lightweight rectification units, and the interface between the detection and recognition branches.",
            "Typical candidate mutations include asymmetric convolutions that enlarge the vertical receptive field, strip-style pooling that preserves elongated text continuity, directional attention blocks that decouple horizontal and vertical context, and lightweight geometric rectification modules that improve recognition-ready alignment. Data preprocessing, optimization settings, and evaluation scripts remain fixed to ensure that architectural changes, not pipeline drift, drive performance differences.",
        ],
        "3.4 LLM-guided autonomous search loop": [
            "At each search iteration, the language model receives the current editable code regions, validation feedback from the previous iteration, and computational feedback such as execution time and memory usage. The prompt also contains task-specific guidance describing degraded vertical text, irregular region geometry, and the need to balance end-to-end accuracy with computational efficiency. Based on this information, the model proposes a modified architecture in source-code form.",
            "Every candidate is passed through a structured validation pipeline. The code is first checked for syntax correctness and compatibility with the existing implementation. The candidate is then trained under a fixed resource budget and evaluated on a held-out validation set using joint spotting criteria. If the candidate fails to compile, violates the resource budget, or underperforms the current incumbent model, it is rejected; otherwise, it becomes the new best model used in the next iteration. This procedure preserves reproducibility while allowing the search process to discover non-standard architecture patterns beyond predefined NAS templates.",
        ],
        "3.5 Joint optimization objective": [
            "The searched model is optimized end to end using a joint loss that combines detection and recognition supervision: L = lambda_det * L_det + lambda_rec * L_rec. Here, L_det denotes the loss of the detection branch, including region classification and/or geometric supervision, and L_rec denotes the sequence-level recognition objective applied to the decoded transcription. In our implementation, the recognition branch is supervised using [CTC / autoregressive decoding loss], depending on the final spotting protocol adopted in the experiment suite.",
            "This joint objective is important because accurate localization alone does not guarantee recognition-ready features, especially for degraded vertical text. By training both branches together, the model is encouraged to preserve structural continuity, region alignment quality, and discriminative sequence information throughout the feature extraction pipeline.",
        ],
        "3.6 Fitness function and budget constraint": [
            "A major challenge in code-level architecture search is preventing uncontrolled growth in model complexity. To address this issue, every candidate architecture is evaluated under a fixed computational budget, defined by a limited training time or iteration budget under the same hardware setting. This discourages the search process from producing overly complex variants that improve optimization behavior at the expense of practical usability.",
            "We define the validation fitness in terms of joint spotting quality. Let M_det denote the detection metric on the validation set, such as Hmean, and let M_e2e denote the end-to-end spotting metric used as the primary model-selection signal. The combined selection score is written as F = alpha * M_det + beta * M_e2e, where alpha and beta balance localization quality and final spotting performance. Detection and recognition sub-metrics are also recorded separately to interpret the source of any improvement. A candidate is accepted only if it improves the validation criterion without violating the resource budget.",
        ],
        "3.7 Characteristics of the searched architecture": [
            "The accepted architectures consistently exhibit stronger directional sensitivity and tighter coupling between detection and recognition than the initial baseline. In particular, the search process favors modules that enlarge the vertical receptive field, improve the compatibility between region-aligned features and sequence decoding, and suppress visually noisy horizontal patterns that are irrelevant to transcription.",
            "Representative retained modules include AsymConvBlock, VerticalBiTrackAttention, Vertical-TPS-Lite, and strip-style pooling. Although each module contributes differently, their combined effect is to reduce region fragmentation in the detection branch and improve sequence continuity in the recognition branch. This suggests that the main benefit of the proposed framework lies in discovering architectural bias that jointly benefits localization and transcription rather than simply increasing model capacity.",
        ],
    }
    for heading, paragraphs in method_sections.items():
        doc.add_heading(heading, level=2)
        for paragraph in paragraphs:
            add_body_paragraph(doc, paragraph)

    doc.add_heading("4. Experimental Setup", level=1)
    exp_sections = {
        "4.1 Datasets": [
            "We organize the experiments around public end-to-end text spotting benchmarks and the Mongolian-Chinese Historical Archive Dataset (MCAD). The public benchmarks are used to assess generalization outside the target domain, while MCAD serves as the primary archival evaluation set. Replace [PUBLIC-BENCHMARK-1], [PUBLIC-BENCHMARK-2], and [PUBLIC-BENCHMARK-3] with the exact benchmark names used in the final experiments.",
            "For MCAD, the final manuscript should report the number of pages, text instances, scripts represented, annotation protocol, and train-validation-test split. Because the paper is framed as joint spotting, the dataset description must explicitly state both detection annotations and transcription availability.",
        ],
        "4.2 Implementation details": [
            "All candidate architectures are implemented in PyTorch and evaluated under the same training pipeline. The final manuscript should report the hardware setup, mixed-precision configuration, optimizer, learning-rate schedule, batch size, input resolution, training budget, and random seeds. These details must remain fixed during the search stage to preserve a fair comparison between architecture variants.",
        ],
        "4.3 Baselines and compared methods": [
            "The main comparison should include representative end-to-end text spotting methods, a manually designed joint baseline, and the final AutoArchival architecture. Each compared method should be accompanied by a short note indicating whether the result comes from the original paper, an official reimplementation, or an in-house rerun under the same protocol.",
        ],
        "4.4 Evaluation metrics": [
            "We report three categories of metrics. Detection quality is measured with Precision, Recall, and Hmean. Recognition quality is measured with [word accuracy / sequence accuracy / normalized edit distance], depending on the benchmark protocol. End-to-end spotting is treated as the primary evaluation view and reported with the official benchmark score or unified end-to-end Hmean. This separation is essential for understanding whether the searched architecture improves region localization, sequence decoding, or both.",
        ],
        "4.5 Ablation settings": [
            "The ablation study is designed to answer three questions: whether LLM-guided search improves over the manually designed joint baseline, which searched modules contribute most to the gains, and how sensitive the final outcome is to the resource budget. The ablation protocol should be identical across all variants except for the factor under study.",
        ],
    }
    for heading, paragraphs in exp_sections.items():
        doc.add_heading(heading, level=2)
        for paragraph in paragraphs:
            add_body_paragraph(doc, paragraph)

    doc.add_heading("5. Results and Discussion", level=1)
    result_sections = {
        "5.1 Comparison with state-of-the-art methods": [
            "Table 1 summarizes the comparison with representative end-to-end text spotting methods and the manually designed baseline. The proposed AutoArchival model should be discussed primarily through the end-to-end spotting score, while detection Hmean and recognition metrics are used to explain where the gain comes from. The discussion should emphasize whether the searched architecture improves localization quality, transcription quality, or both.",
        ],
        "5.2 Results on public text spotting benchmarks": [
            "The public benchmark results establish whether the discovered architecture generalizes beyond the archival domain. For each benchmark, report the official end-to-end spotting score first, followed by the supporting detection and recognition metrics. Use this subsection to analyze whether the searched vertical-aware modules still help on more general irregular-text datasets or whether the main gains are concentrated in archival settings.",
        ],
        "5.3 Results on MCAD": [
            "MCAD is the primary target domain of the proposed framework. This subsection should explain how the searched model behaves on vertically arranged Mongolian text, mixed-script layouts, and degraded pages. The key comparison should highlight whether the joint search process improves sequence continuity and region completeness relative to the baseline and externally compared methods.",
        ],
        "5.4 Ablation study": [
            "The ablation study should report at least four variants: the manually designed baseline, the baseline plus individual searched modules, the best searched architecture without the recognition-specific alignment improvement, and the full AutoArchival model. The discussion should identify which modules mainly affect detection, which affect recognition, and which improve the final end-to-end score by coordinating both branches.",
        ],
        "5.5 Efficiency analysis": [
            "Because AutoArchival includes a search stage, the final paper should separate search cost from deployment cost. Search cost should be reported in GPU hours or total budgeted iterations, while deployment cost should be summarized with parameter count, FLOPs, and inference speed. This subsection should make clear that the fixed-budget search is intended to keep the final searched model compact and practical.",
        ],
        "5.6 Qualitative results": [
            "Qualitative examples should compare the baseline and the searched architecture on representative pages from both public benchmarks and MCAD. The figure panel should highlight complete text region detection, cleaner alignment for vertical Mongolian text, and improved transcription quality under degradation. Whenever possible, use side-by-side visualizations that jointly show predicted boxes or masks and decoded text strings.",
        ],
        "5.7 Failure cases and discussion": [
            "The final discussion should acknowledge the remaining failure modes, such as extremely blurred text, heavily overlapping instances, ambiguous seals, and incomplete transcriptions under severe corruption. Use these cases to explain the current limitations of the search framework and to motivate future work on larger archive-specific datasets, better recognition supervision, and more interpretable search constraints.",
        ],
    }
    for heading, paragraphs in result_sections.items():
        doc.add_heading(heading, level=2)
        for paragraph in paragraphs:
            add_body_paragraph(doc, paragraph)

    add_table(
        doc,
        "Table 1. Comparison with representative end-to-end text spotting methods on public benchmarks.",
        [
            "Method",
            "Benchmark",
            "Det. P",
            "Det. R",
            "Det. Hmean",
            "Rec. Acc./NED",
            "End-to-End Score",
            "Params (M)",
        ],
        [
            ["[Method A]", "[PUBLIC-BENCHMARK-1]", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]"],
            ["[Method B]", "[PUBLIC-BENCHMARK-1]", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]"],
            ["Joint baseline", "[PUBLIC-BENCHMARK-1]", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]"],
            ["AutoArchival", "[PUBLIC-BENCHMARK-1]", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]"],
        ],
    )

    add_table(
        doc,
        "Table 2. Joint spotting results on the Mongolian-Chinese Historical Archive Dataset (MCAD).",
        [
            "Method",
            "Det. P",
            "Det. R",
            "Det. Hmean",
            "Rec. Acc./NED",
            "End-to-End Score",
            "Notes",
        ],
        [
            ["[Method A]", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]", "[external / rerun]"],
            ["Joint baseline", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]", "[manual design]"],
            ["AutoArchival", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]", "[searched model]"],
        ],
    )

    add_table(
        doc,
        "Table 3. Ablation study on the contribution of searched modules and branch coupling.",
        [
            "Variant",
            "Det. Hmean",
            "Rec. Acc./NED",
            "End-to-End Score",
            "Search Cost",
        ],
        [
            ["Baseline", "[XX.X]", "[XX.X]", "[XX.X]", "-"],
            ["Baseline + AsymConvBlock", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]"],
            ["Baseline + VerticalBiTrackAttention", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]"],
            ["Baseline + alignment refinement", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]"],
            ["AutoArchival", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]"],
        ],
    )

    add_table(
        doc,
        "Table 4. Search cost and deployment efficiency of the main model variants.",
        [
            "Model",
            "Search Cost (GPU hrs)",
            "Params (M)",
            "FLOPs (G)",
            "FPS",
            "End-to-End Score",
        ],
        [
            ["Joint baseline", "-", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]"],
            ["Intermediate searched model", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]"],
            ["AutoArchival", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]", "[XX.X]"],
        ],
    )

    add_placeholder_figure(
        doc,
        "Figure 1",
        "Figure 1. Overview of the AutoArchival framework for joint historical document text spotting, including the editable search regions, fixed training loop, and end-to-end evaluation pathway.",
    )
    add_placeholder_figure(
        doc,
        "Figure 2",
        "Figure 2. Search trajectory under the fixed-budget evaluation protocol. Replace with the final validation curve and clearly distinguish surrogate search metrics from final end-to-end reporting metrics.",
    )
    add_placeholder_figure(
        doc,
        "Figure 3",
        "Figure 3. The final searched joint architecture, highlighting directional feature extraction, region alignment, and recognition-aware branch coupling.",
    )
    add_placeholder_figure(
        doc,
        "Figure 4",
        "Figure 4. Qualitative comparisons and representative failure cases on public benchmarks and MCAD. Show predicted regions together with decoded transcriptions.",
    )

    doc.add_heading("6. Conclusion", level=1)
    conclusion = [
        "We presented AutoArchival, a budget-constrained LLM-guided code-level architecture search framework for Mongolian-Chinese historical document text spotting. By treating end-to-end spotting as the primary evaluation target while separately reporting detection and recognition sub-metrics, the framework makes it possible to analyze how architecture changes influence both localization and transcription. The searched model is designed to preserve vertical text continuity, improve region alignment, and strengthen the interaction between the detection and recognition branches under realistic computational limits.",
        "The final manuscript should summarize the measured gains on public benchmarks and MCAD using verified end-to-end spotting results. At the same time, the discussion should remain explicit about the remaining limitations, including severe archive degradation, limited annotation diversity, and the sensitivity of recognition quality to alignment errors. These limitations motivate future work on larger benchmark coverage, richer archive-specific supervision, and more interpretable search constraints for joint spotting systems.",
    ]
    for paragraph in conclusion:
        add_body_paragraph(doc, paragraph)

    doc.add_heading("References", level=1)
    for ref in REFERENCES:
        p = doc.add_paragraph(style="Normal")
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(2)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.add_run(ref)

    out_path = OUT_DIR / "paper_draft_PR_joint_spotting.docx"
    doc.save(out_path)


def build_title_page():
    doc = Document()
    configure_document(doc)

    title = doc.add_paragraph(style="Title")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.add_run(TITLE)

    blocks = [AUTHOR_LINE, *AFFILIATIONS, CORRESPONDING_AUTHOR, *ADDITIONAL_EMAILS, f"Short title: {SHORT_TITLE}"]
    for block in blocks:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.5
        run = p.add_run(block)
        run.font.name = "Times New Roman"
        run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
        run.font.size = Pt(10)

    doc.add_heading("Author roles and notes", level=1)
    notes = [
        f"CRediT authorship contribution statement: {CREDIT_STATEMENT}",
        f"Funding: {FUNDING_STATEMENT}",
        f"Declaration of competing interest: {COMPETING_INTEREST_STATEMENT}",
        f"Declaration of generative AI in scientific writing: {AI_DECLARATION}",
    ]
    for note in notes:
        add_body_paragraph(doc, note)

    doc.add_heading("Author Biographies", level=1)
    for biography in AUTHOR_BIOS:
        add_body_paragraph(doc, biography)

    doc.save(OUT_DIR / "title_page_PR_joint_spotting.docx")


def write_text_file(name: str, text: str):
    (OUT_DIR / name).write_text(text.strip() + "\n", encoding="utf-8")


def build_submission_materials():
    cover_letter = f"""
Dear Editors of Pattern Recognition,

We would like to submit the manuscript entitled "{TITLE}" by Lanying Liang, Yuefeng Liu, and Jianjun Zhao for consideration as a regular research article in Pattern Recognition.

This work addresses joint text detection and text spotting in Mongolian-Chinese historical archives, a challenging pattern recognition problem characterized by vertically arranged text, severe degradation, mixed-script layouts, and limited annotated data. Existing end-to-end text spotting frameworks are largely tuned for natural scenes and often transfer poorly to archival documents with strong directional structure. To address this gap, we propose AutoArchival, a budget-constrained LLM-guided code-level architecture search framework that discovers task-specific modules for joint localization and transcription under explicit computational limits.

The manuscript fits the scope of Pattern Recognition because it focuses on model design, end-to-end recognition performance, and structured visual pattern analysis for a difficult real-world document domain. The contribution is not simply the use of a language model; rather, it is a constrained architecture search strategy that improves the coupling between detection and recognition for historical text spotting.

In the final submission package, the paper reports:
- comparisons with representative state-of-the-art end-to-end text spotting methods;
- evaluation on public text spotting benchmarks and the Mongolian-Chinese Historical Archive Dataset (MCAD);
- standard detection, recognition, and end-to-end spotting metrics under a unified reporting scheme.

We confirm that this manuscript is original, has not been published previously, and is not under consideration for publication elsewhere. All authors have approved the manuscript and agree with its submission to Pattern Recognition.

Thank you for your consideration.

Sincerely,
Yuefeng Liu
School of Artificial Intelligence and Data Science, Inner Mongolia University of Science and Technology
liuyuefeng@imust.edu.cn
On behalf of Lanying Liang, Yuefeng Liu, and Jianjun Zhao
"""
    write_text_file("cover_letter_PR_joint_spotting.txt", cover_letter)

    highlights = """
- LLM-guided search discovers joint spotting architectures for archival text
- A fixed budget constrains code-level architecture search and model growth
- Vertical-aware modules improve localization-transcription coupling
- Public benchmarks and MCAD evaluate end-to-end spotting performance
- Ablations analyze search strategy, module gains, and efficiency trade-offs
"""
    write_text_file("highlights_PR_joint_spotting.txt", highlights)

    data_statement = """
Public benchmark datasets (ICDAR 2015, Total-Text) used in this study are available from their respective original sources.

The Mongolian-Chinese Historical Archive Dataset (MCAD) introduced in this study, along with its fine-grained annotations, as well as the complete code, model configurations, and experiment scripts for the AutoArchival framework, will be publicly released at https://github.com/liuyuefeng/AutoArchival upon the acceptance of this paper to facilitate future research.
"""
    write_text_file("data_availability_statement_PR_joint_spotting.txt", data_statement)

    declarations = """
Funding
This work was supported by the National Natural Science Foundation of China (Grant No. 62341604), the Science and Technology Project of Inner Mongolia Autonomous Region Archives Bureau (Grant No. 2022-36), the China Scholarship Council (Grant No. 202408150080), and the General Project of the 14th Five-Year Plan for Educational Science of Inner Mongolia Autonomous Region (Grant No. NGJGH2025013).

CRediT authorship contribution statement
Lanying Liang: Conceptualization, Data Curation, Writing - Original Draft. Yuefeng Liu: Methodology, Software, Validation, Writing - Review & Editing, Supervision. Jianjun Zhao: Writing - Review & Editing, Supervision.

Declaration of competing interest
The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

Declaration of generative AI in scientific writing
Generative AI technologies (Claude/Gemini) were used solely for manuscript formatting and grammatical polishing.

Acknowledgements
The authors would like to thank the Inner Mongolia Autonomous Region Archives Bureau for their support.
"""
    write_text_file("author_declarations_PR_joint_spotting.txt", declarations)

    notes = """
Submission package generated by build_pr_joint_submission.py

Files
- paper_draft_PR_joint_spotting.docx
- title_page_PR_joint_spotting.docx
- cover_letter_PR_joint_spotting.txt
- highlights_PR_joint_spotting.txt
- data_availability_statement_PR_joint_spotting.txt
- author_declarations_PR_joint_spotting.txt

Before submission
1. Replace all bracketed placeholders such as [XX.X], [PUBLIC-BENCHMARK-1], and [CTC / autoregressive decoding loss].
2. Insert the final figures into the manuscript and update captions if needed.
3. Verify that the metrics reported in the text, tables, and cover letter are identical.
4. Recheck author metadata, affiliations, and declarations if the submission team changes.
5. Export the final PDF and check page numbers, captions, and reference formatting.
"""
    write_text_file("README_submission_notes.txt", notes)


def main():
    OUT_DIR.mkdir(exist_ok=True)
    build_manuscript()
    build_title_page()
    build_submission_materials()


if __name__ == "__main__":
    main()
