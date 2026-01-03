# ============================================================================
# FILE: reports/reports.py  (NEW FILE - Create this folder and file)
# Generates PDF reports for experiments
# ============================================================================

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import config
from visualization.charts import ChartGenerator
from visualization.punnett_square import PunnettSquareVisualizer


class PDFReportGenerator:
    """
    Generates professional PDF reports for genetics experiments.
    """
    
    @staticmethod
    def generate_report(experiment, output_path=None):
        """
        Generate a complete PDF report for an experiment.
        
        Args:
            experiment: Experiment object to generate report for
            output_path: Where to save PDF (auto-generated if None)
            
        Returns:
            Path to saved PDF file
        """
        if output_path is None:
            output_path = config.EXPORTS_DIR / f"{experiment.experiment_id}_Report.pdf"
        
        # Create PDF document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Container for PDF elements
        story = []
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        title = Paragraph(f"Genetics Experiment Report<br/>{experiment.name}", title_style)
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Experiment Details Section
        story.append(Paragraph("Experiment Details", heading_style))
        
        details_data = [
            ['Experiment ID:', experiment.experiment_id],
            ['Date Created:', experiment.date_created.strftime('%Y-%m-%d %H:%M')],
            ['Status:', experiment.get_status()],
            ['Parent 1 Genotype:', str(experiment.parent1)],
            ['Parent 2 Genotype:', str(experiment.parent2)],
        ]
        
        details_table = Table(details_data, colWidths=[2*inch, 4*inch])
        details_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        story.append(details_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Allele Definitions Section
        story.append(Paragraph("Allele Definitions", heading_style))
        
        allele_data = [['Symbol', 'Description', 'Type']]
        for symbol, allele in sorted(experiment.allele_definitions.items()):
            allele_type = 'Dominant' if allele.is_dominant else 'Recessive'
            allele_data.append([symbol, allele.description, allele_type])
        
        allele_table = Table(allele_data, colWidths=[1*inch, 3.5*inch, 1.5*inch])
        allele_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ECF0F1')])
        ]))
        
        story.append(allele_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Expected Ratios Section
        story.append(Paragraph("Expected Phenotype Ratios", heading_style))
        
        expected_data = [['Phenotype', 'Expected Count', 'Percentage']]
        for phenotype, count in experiment.expected_counts.items():
            percentage = (count / experiment.total_expected) * 100
            expected_data.append([phenotype, f"{count:.1f}", f"{percentage:.1f}%"])
        
        expected_table = Table(expected_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        expected_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ECF0F1')])
        ]))
        
        story.append(expected_table)
        story.append(Spacer(1, 0.3*inch))
        # Punnett Square Visualization Section (INSERT THIS)
        story.append(Paragraph("Punnett Square", heading_style))
        
        try:
            punnett_path = PunnettSquareVisualizer.create_punnett_square(experiment)
            if punnett_path.exists():
                # Scale image based on number of gametes
                parent1_gametes = experiment.parent1.get_gametes()
                parent2_gametes = experiment.parent2.get_gametes()
                
                # Adjust size based on complexity
                if len(parent1_gametes) <= 2 and len(parent2_gametes) <= 2:
                    img_width = 4 * inch
                    img_height = 4 * inch
                else:
                    img_width = 6 * inch
                    img_height = 6 * inch
                
                img = Image(str(punnett_path), width=img_width, height=img_height)
                story.append(img)
                story.append(Spacer(1, 0.3*inch))
        except Exception as e:
            error_text = Paragraph(f"Could not generate Punnett Square: {str(e)}", styles['Normal'])
            story.append(error_text)
            story.append(Spacer(1, 0.3*inch))
            
        # Observations and Analysis Section (only if experiment is complete)
        if experiment.is_complete():
            story.append(Paragraph("Observed Results", heading_style))
            
            observed_data = [['Phenotype', 'Expected', 'Observed', 'Difference']]
            for phenotype in experiment.expected_counts.keys():
                expected = experiment.expected_counts[phenotype]
                observed = experiment.observed_counts[phenotype]
                diff = observed - expected
                observed_data.append([
                    phenotype, 
                    f"{expected:.1f}", 
                    str(observed), 
                    f"{diff:+.1f}"
                ])
            
            observed_table = Table(observed_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            observed_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ECF0F1')])
            ]))
            
            story.append(observed_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Statistical Analysis Section
            if experiment.chi_square_result:
                story.append(Paragraph("Statistical Analysis (Chi-Square Test)", heading_style))
                
                result = experiment.chi_square_result
                
                stats_data = [
                    ['Chi-Square Value:', f"{result['chi_square']}"],
                    ['P-Value:', f"{result['p_value']}"],
                    ['Degrees of Freedom:', str(result['degrees_freedom'])],
                    ['Critical Value (α=0.05):', f"{result['critical_value']}"],
                    ['Result:', 'PASS ✓' if result['passed'] else 'FAIL ✗']
                ]
                
                stats_table = Table(stats_data, colWidths=[2.5*inch, 3.5*inch])
                stats_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
                ]))
                
                story.append(stats_table)
                story.append(Spacer(1, 0.2*inch))
                
                # Interpretation
                interpretation = Paragraph(
                    f"<b>Interpretation:</b> {result['interpretation']}", 
                    styles['Normal']
                )
                story.append(interpretation)
                story.append(Spacer(1, 0.3*inch))
            
            # Generate and include charts
            story.append(PageBreak())
            story.append(Paragraph("Visualizations", heading_style))
            
            try:
                # Generate bar chart
                bar_chart_path = ChartGenerator.create_bar_chart(experiment)
                if bar_chart_path.exists():
                    story.append(Spacer(1, 0.2*inch))
                    img = Image(str(bar_chart_path), width=6*inch, height=3.6*inch)
                    story.append(img)
                    story.append(Spacer(1, 0.3*inch))
                
                # Generate pie chart
                pie_chart_path = ChartGenerator.create_pie_chart(experiment)
                if pie_chart_path.exists():
                    story.append(Spacer(1, 0.2*inch))
                    img = Image(str(pie_chart_path), width=4*inch, height=4*inch)
                    story.append(img)
            except Exception as e:
                error_text = Paragraph(f"Could not generate charts: {str(e)}", styles['Normal'])
                story.append(error_text)
        
        else:
            no_data = Paragraph(
                "<i>No observations have been recorded for this experiment yet.</i>", 
                styles['Normal']
            )
            story.append(no_data)
            story.append(Spacer(1, 0.2*inch))
        
        # Notes Section
        if experiment.notes:
            story.append(Spacer(1, 0.3*inch))
            story.append(Paragraph("Notes", heading_style))
            notes_text = Paragraph(experiment.notes, styles['Normal'])
            story.append(notes_text)
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer = Paragraph(
            f"<i>Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>"
            f"Fruit Fly Genetics Tracker v{config.APP_VERSION}</i>",
            ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
        )
        story.append(footer)
        
        # Build PDF
        doc.build(story)
        
        return output_path