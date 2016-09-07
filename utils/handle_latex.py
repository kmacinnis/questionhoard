import os
from subprocess import Popen, PIPE
from tempfile import mkstemp
 
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.template import RequestContext
 
def return_pdf(request, template, dictionary, filename):
    # render latex template and vars to a string
    latex = render_to_string(template, dictionary, context_instance=None)
 
    # create a unique temorary filename
    fd, path = mkstemp(prefix="latex_", suffix=".pdf")
    folder, fname = os.path.split(path)
    jobname, ext = os.path.splitext(fname)  # jobname is just the filename without .pdf, it's what pdflatex uses
 
    # for the TOC to be built, pdflatex must be run twice, on the second run it will generate a .toc file
    for i in range(2):
        # start pdflatex, we can send the tex file from stdin, but the output file can only be saved to disk, not piped to stdout unfortunately/
        process = Popen(["pdflatex", "-output-directory", folder, "-jobname", jobname], stdin=PIPE, stdout=PIPE)  # piping stdout suppresses output messages
        process.communicate(latex.encode())
 
    # open the temporary pdf file for reading.
    try:
        pdf = os.fdopen(fd, "rb")
        output = pdf.read()
        pdf.close()
    except OSError:
        raise Http404("Error generating PDF file")  # maybe we should use an http  500 here, 404 makes no sense
 
    # generate the response with pdf attachment
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; filename=" + filename
    response.write(output)
 
    # delete the pdf from temp directory, and other generated files ending on .aux and .log
    for ext in (".pdf", ".aux", ".log", ".toc", ".lof", ".lot", ".synctex.gz"):
        try:
            os.remove(os.path.join(folder, jobname) + ext)
        except OSError:
            pass
 
    # return the response
    return response
    
    
    
def return_tex(request, template, dictionary, filename):
    # render latex template and vars to a string
    latex = render_to_string(template, dictionary, context_instance=None)
    
    
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'inline; filename="%s.txt"' % filename
    response.write(latex)

    return response
