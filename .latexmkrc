@default_files = ('cv_template_en.tex');

$aux_dir = 'out';
$emulate_aux = 1;
$do_cd = 1;

$pdflatex=q/xelatex -synctex=1 %O %S/;
$pdf_mode = 1;
$dvi_mode = $postscript_mode = 0;
