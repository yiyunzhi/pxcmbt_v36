from _dev.help_generator.run import task_build_mbt_help_html,task_build_mbt_dev_help_html
from _dev.i18n.run import i18n_framework_do_po,i18n_mbt_do_po
# --------------------------------------------------------------
# ref
# --------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/tutorial/automatic-doc-generation.html

# --------------------------------------------------------------
# task for generating mbt help document
# --------------------------------------------------------------
print('start the task mbt help doc generation')
_ret,_content=task_build_mbt_help_html()
print(_content)
print('successful' if _ret==0 else 'failed')
# --------------------------------------------------------------
# task for generating mbt dev help document
# --------------------------------------------------------------
print('start the task mbt dev help doc generation')
_ret,_content=task_build_mbt_dev_help_html()
print(_content)
print('successful' if _ret==0 else 'failed')
# --------------------------------------------------------------
# task for generating framework i18n document
# --------------------------------------------------------------
print('start the task framework i18n doc generation')
_ret,_content=i18n_framework_do_po()
print(_content)
print('successful' if _ret==0 else 'failed')
# --------------------------------------------------------------
# task for generating mbt i18n document
# --------------------------------------------------------------
print('start the task framework i18n doc generation')
_ret,_content=i18n_mbt_do_po()
print(_content)
print('successful' if _ret==0 else 'failed')