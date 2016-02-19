import glob
from xml.dom import minidom
import sys

path=""
xmls=0
sumSub=0
sumTotal=0
sumImp=0

total = len(sys.argv)
if total==1:
	print "\n\n************************ Factura Script *****************************************\n"
	print "  MINIMO Tienes que dar el post-fijo del nombre al archivo (Facturas_<arg>.csv)\n"
	print "  Usa el parametro ? para ayuda\n"
	exit()
elif total>1:
	if sys.argv[1]=='?':
		print "\n\n************************ Factura Script *********************************\n"
		print "  DESCRIPCION"
		print "  Este script busca todos los XML de facturacion, ya sea en donde"
		print "  se encuentre o en el path dado y escupe informacion en un CSV"
		print "  para que hagas tus cuentas en Excel o algo.\n"
		print "  CSV = RFC Emisor, Fecha, Subtotal, Impuesto, Total\n"
		print "  USO:"
		print "  El primer parametro a pasar es el post-fijo al nombre del CSV "
		print "  El segundo parametro es el path a seguir para encontrar los XML"
		print "  que se va a generar\n"
		print "\tfacturaParser.py <post-fijo> <directorio>\n"
		print "  ejemplos:\n"
		print "\tfacturaParser.py enero-diciembre\n"
		print "\tfacturaParser.py enero-diciembre carpeta1\n"
		print "  Esto generara un archivo llamado Facturas_enero-diciembre.csv"
		print "\n************************ Factura Script *********************************\n"
		exit();
	else:
		print "\n\n************************ Factura Script *********************************\n"
		print "   INICIANDO SCRIPT\n"
		csv = open("Facturas_"+sys.argv[1]+".csv","a")
		csv.seek(0, 2)
		length = csv.tell()
		if(length==0):
			csv.write('Emisor,fecha,Sub Total, Impuesto, Total\n')
		else:
			print "   El archivo: Facturas_"+sys.argv[1]+".csv ya existe\n"
			
		if(total==3):
			path=sys.argv[2]+"/";
		files=glob.glob(path+"*.xml")
		for name in files:
			tmpXml= minidom.parse(name)
			comprobante = tmpXml.getElementsByTagName('cfdi:Comprobante')
			fecha = comprobante[0].attributes['fecha'].value
			subTotal = comprobante[0].attributes['subTotal'].value
			sumSub+=float(subTotal)
			
			total = comprobante[0].attributes['total'].value
			sumTotal+=float(total)
			
			impuesto= float(total)-float(subTotal)
			sumImp+=float(impuesto)
			
			emisor = tmpXml.getElementsByTagName('cfdi:Emisor')
			rfc=emisor[0].attributes['rfc'].value
			xmls=xmls+1
			
			csv.write(rfc+ "," + fecha + ","+ subTotal + "," +str(impuesto)+ "," + total + "\n")
			
		csv.close()
		print '   SCRIP TERMINADO\n'
		print '   TOTALES'
		print '   Archivos XML Procesados:'+str(xmls)
		print '   Suma SubTotal: $'+str(sumSub)
		print '   Suma Impuestos: $'+str(sumImp)
		print '   Suma Total: $'+str(sumTotal)
		print "\n\n************************ Factura Script *********************************\n"
