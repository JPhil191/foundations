from waitress import serve
import irtp.__init__

serve(irtp.__init__.app, host='0.0.0.0', port=80)
