<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">

	<html>
	<head>
	</head>
	<body>
	<h1>Contact information for <b><xsl:value-of select="me/name" /></b></h1>

	<h2>Mailing address:</h2>
	<xsl:value-of select="me/address" />

	<h2>Phone:</h2>
	<xsl:value-of select="me/tel" />

	<h2>Email address:</h2>
	<xsl:value-of select="me/email" />

	<h2>Web site URL:</h2>
	<xsl:value-of select="me/url" />

	</body>
	</html>

</xsl:template>
</xsl:stylesheet>
