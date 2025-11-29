"""
PDF Report Generation Service

This module provides services for generating professional PDF reports
summarizing fact-checking results. It uses ReportLab to style and lay out
tables, paragraphs, and logo banners with verdicts, confidence scores,
explanations, votes, and sources relating to a given claim.

Main Components:

- Utility functions for formatting (dates, stripping HTML, verdict color).
- Parsing of explanations to extract sources.
- Custom styled ReportLab objects for presenting information in the PDF.
- The main `generate_pdf_report()` function, which accepts `AggregatedResult`
  and returns a BytesIO PDF.
"""

import re
from datetime import datetime
from html import unescape
from io import BytesIO
from typing import List, Tuple

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from src.app.models.schemas import AggregatedResult, Verdict


def _create_logo_table(styles) -> Table:
    """
    Helper to create a styled logo table with FactScreen logo and subtitle for the PDF header.
    """
    logo_data = [
        [
            Paragraph(
                "<b>✓</b>",
                ParagraphStyle(
                    "LogoIcon",
                    parent=styles["Normal"],
                    fontSize=32,
                    textColor=colors.HexColor("#6366f1"),
                    alignment=1,  # Center icon
                ),
            ),
            Paragraph(
                (
                    "<b>FactScreen</b><br/>"
                    "<font size='9' color='#64748b'>Fact-Checking Platform</font>"
                ),
                ParagraphStyle(
                    "LogoText",
                    parent=styles["Normal"],
                    fontSize=20,
                    textColor=colors.HexColor("#1e293b"),
                    alignment=0,  # Left-aligned text
                    leading=22,
                ),
            ),
        ]
    ]

    logo_table = Table(logo_data, colWidths=[1 * inch, 5 * inch])
    logo_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (0, 0), "CENTER"),
                ("ALIGN", (1, 0), (1, 0), "LEFT"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return logo_table


def _get_verdict_color(verdict: Verdict) -> colors.Color:
    """
    Get a visual color highlight for the given fact-check verdict.
    """
    color_map = {
        Verdict.TRUE: colors.HexColor("#22c55e"),  # Green
        Verdict.MISLEADING: colors.HexColor("#ef4444"),  # Red
        Verdict.UNKNOWN: colors.HexColor("#eab308"),  # Yellow
    }
    return color_map.get(verdict, colors.HexColor("#6b7280"))  # Default gray


def _format_confidence(confidence: float) -> str:
    """
    Format a confidence score as a percentage, e.g., 0.85 -> '85.0%'
    """
    return f"{confidence * 100:.1f}%"


def _format_date() -> str:
    """
    Return the current date/time in human-readable form for the report.
    """
    return datetime.now().strftime("%B %d, %Y at %I:%M %p")


def _strip_html_tags(text: str) -> str:
    """
    Remove HTML tags and decode HTML entities for safe PDF rendering.
    """
    text = re.sub(r"<[^>]+>", "", text)  # Strip HTML
    text = unescape(text)  # Decode HTML entities
    return text.strip()


def _parse_sources_from_explanation(explanation: str) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Parse 'Sources:' section from the explanation string.

    Extracts a list of (title, URL) tuples from lines found after the 'Sources:' block if present.
    Lines are assumed to be in the format:
        - SourceName | verdict: X | snippet: Title | URL

    Returns:
        (main_explanation_text, list_of_sources)
    """
    sources = []
    main_text = explanation

    if "Sources:" in explanation:
        parts = explanation.split("Sources:", maxsplit=1)
        main_text = parts[0].strip()
        sources_block = parts[1].strip() if len(parts) > 1 else ""

        # Split sources into lines and parse each line
        lines = [line.strip() for line in sources_block.splitlines() if line.strip()]
        seen = set()

        for line in lines:
            line = line.lstrip("- ").strip()  # Remove leading dash
            if not line:
                continue
            if "|" in line:
                parts = [p.strip() for p in line.split("|")]
                title = None
                url = None
                for part in parts:
                    if part.startswith("snippet:"):
                        title = part.replace("snippet:", "").strip()
                    elif part.startswith("http"):
                        url = part
                    elif not part.startswith(("verdict:", "snippet:")) and not title:
                        # Use as fallback title
                        if not any(p.startswith("verdict:") for p in parts):
                            title = part
                # More fallback title logic (find first non-metadata part)
                if not title:
                    for part in parts:
                        if not part.startswith(("verdict:", "snippet:")) and not part.startswith(
                            "http"
                        ):
                            title = part
                            break
                if not title:
                    title = url if url and len(url) < 60 else "Source"
                key = (title.lower(), url.lower() if url else "")
                if key not in seen:
                    sources.append((title, url or ""))
                    seen.add(key)
            elif line.startswith("http"):
                title = line if len(line) < 60 else line[:57] + "..."
                key = (title.lower(), line.lower())
                if key not in seen:
                    sources.append((title, line))
                    seen.add(key)
            elif line:
                key = (line.lower(), "")
                if key not in seen:
                    sources.append((line, ""))
                    seen.add(key)
    return main_text, sources


def generate_pdf_report(result: AggregatedResult) -> BytesIO:
    """
    Generate a stylized PDF report for a given fact-check result.

    Args:
        result: AggregatedResult with all information to be included.

    Returns:
        BytesIO: A buffer containing the PDF report that can be sent as a file.
    """
    # Output PDF will be built into this in-memory buffer for streaming/download
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
    )
    story = []
    styles = getSampleStyleSheet()

    # ParagraphStyles setup for various heading and body elements
    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=16,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=8,
        spaceBefore=12,
    )
    subheading_style = ParagraphStyle(
        "CustomSubheading",
        parent=styles["Heading3"],
        fontSize=12,
        textColor=colors.HexColor("#475569"),
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#334155"),
        leading=14,
    )

    # Add logo banner/header
    logo_table = _create_logo_table(styles)
    story.append(logo_table)
    story.append(Spacer(1, 0.15 * inch))
    story.append(
        Paragraph(
            "Fact-Checking Report",
            ParagraphStyle(
                "ReportTitle",
                parent=styles["Heading2"],
                fontSize=18,
                textColor=colors.HexColor("#1e293b"),
                spaceAfter=8,
                alignment=1,
            ),
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    # Metadata section: report generated time and claim text
    metadata_data = [
        ["Report Generated:", _format_date()],
        ["Claim Analyzed:", result.claim_text],
    ]
    metadata_table = Table(metadata_data, colWidths=[2 * inch, 4.5 * inch])
    metadata_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f1f5f9")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1e293b")),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ]
        )
    )
    story.append(metadata_table)
    story.append(Spacer(1, 0.3 * inch))

    # Final verdict and confidence score highlight section
    verdict_color = _get_verdict_color(result.verdict)
    verdict_text = result.verdict.value.upper()
    confidence_text = _format_confidence(result.confidence)

    bold_style = ParagraphStyle(
        "BoldStyle",
        parent=body_style,
        fontName="Helvetica-Bold",
        fontSize=12,
    )

    verdict_data = [
        [
            "Final Verdict:",
            Paragraph(
                verdict_text,
                ParagraphStyle("VerdictBold", parent=bold_style, textColor=colors.white),
            ),
        ],
        ["Confidence Score:", Paragraph(confidence_text, bold_style)],
    ]
    verdict_table = Table(verdict_data, colWidths=[2 * inch, 4.5 * inch])
    verdict_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f1f5f9")),
                ("BACKGROUND", (1, 0), (1, 0), verdict_color),
                ("TEXTCOLOR", (1, 0), (1, 0), colors.white),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1e293b")),
                ("TEXTCOLOR", (1, 1), (1, 1), colors.HexColor("#1e293b")),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
            ]
        )
    )
    story.append(Paragraph("Analysis Summary", heading_style))
    story.append(verdict_table)
    story.append(Spacer(1, 0.2 * inch))

    # If votes breakdown is available, show per-verdict vote counts
    if result.votes:
        story.append(Paragraph("Verdict Breakdown", subheading_style))
        votes_data = [["Verdict", "Count"]]
        for verdict, count in result.votes.items():
            votes_data.append([verdict.value.title(), str(count)])

        votes_table = Table(votes_data, colWidths=[3 * inch, 3.5 * inch])
        votes_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 11),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [colors.white, colors.HexColor("#f8fafc")],
                    ),
                ]
            )
        )
        story.append(votes_table)
        story.append(Spacer(1, 0.3 * inch))

    # Main explanation and extracted sources
    if result.explanation:
        story.append(Paragraph("Detailed Explanation", heading_style))
        main_text, sources_list = _parse_sources_from_explanation(result.explanation)
        main_text = _strip_html_tags(main_text)
        main_text = main_text.replace("**", "").replace("__", "").replace("*", "")
        paragraphs = [p.strip() for p in main_text.split("\n\n") if p.strip()]
        for para in paragraphs:
            story.append(Paragraph(para, body_style))
            story.append(Spacer(1, 0.1 * inch))
        if sources_list:
            story.append(Spacer(1, 0.2 * inch))
            story.append(Paragraph("Sources", subheading_style))
            sources_data = [["#", "Source", "Link"]]
            for idx, (title, url) in enumerate(sources_list, start=1):
                title_clean = _strip_html_tags(title)
                if len(title_clean) > 60:
                    title_clean = title_clean[:57] + "..."
                url_display = (
                    url if url and len(url) <= 50 else (url[:47] + "..." if url else "N/A")
                )
                sources_data.append([str(idx), title_clean, url_display])
            sources_table = Table(sources_data, colWidths=[0.4 * inch, 3.5 * inch, 2.6 * inch])
            sources_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                        ("ALIGN", (0, 0), (0, -1), "CENTER"),
                        ("ALIGN", (1, 0), (1, -1), "LEFT"),
                        ("ALIGN", (2, 0), (2, -1), "LEFT"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 10),
                        ("FONTSIZE", (0, 1), (-1, -1), 9),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                        ("TOPPADDING", (0, 0), (-1, -1), 6),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                        (
                            "ROWBACKGROUNDS",
                            (0, 1),
                            (-1, -1),
                            [colors.white, colors.HexColor("#f8fafc")],
                        ),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ]
                )
            )
            story.append(sources_table)
        story.append(Spacer(1, 0.3 * inch))

    # Table of individual provider results if present
    if result.provider_results:
        story.append(Paragraph("Source Analysis", heading_style))
        provider_data = [["Provider", "Verdict", "Rating", "Source"]]
        for provider_result in result.provider_results:
            provider_name = provider_result.provider.value.replace("_", " ").title()
            verdict = provider_result.verdict.value.title()
            rating = provider_result.rating or "N/A"
            source = provider_result.source_url or "N/A"
            if len(str(source)) > 40:
                source = str(source)[:37] + "..."
            provider_data.append([provider_name, verdict, rating, str(source)])
        provider_table = Table(
            provider_data, colWidths=[1.5 * inch, 1.2 * inch, 1.5 * inch, 2.3 * inch]
        )
        provider_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 10),
                    ("FONTSIZE", (0, 1), (-1, -1), 9),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [colors.white, colors.HexColor("#f8fafc")],
                    ),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )
        story.append(provider_table)
        story.append(Spacer(1, 0.3 * inch))

    # Footer with disclaimer
    story.append(Spacer(1, 0.2 * inch))
    footer_text = (
        "<i>This report was generated automatically by FactScreen. "
        "The analysis is based on multiple fact-checking sources and AI-powered classification. "
        "Please verify critical information independently.</i>"
    )
    story.append(
        Paragraph(
            footer_text,
            ParagraphStyle(
                "Footer", parent=body_style, fontSize=8, textColor=colors.HexColor("#64748b")
            ),
        )
    )

    # Finalize and return PDF buffer
    doc.build(story)
    buffer.seek(0)
    return buffer
