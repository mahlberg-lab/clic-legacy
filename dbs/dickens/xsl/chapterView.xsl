<?xml version="1.0"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

	
	<xsl:variable name="upper">ABCDEFGHIJKLMNOPQRSTUVWXYZ</xsl:variable>
	<xsl:variable name="lower">abcedfghijklmnopqrstuvwxyz</xsl:variable>
	


	<xsl:template match="/">
		<xsl:apply-templates select="//div"/>  
	</xsl:template>


	<xsl:template match="div[@type='chapter']">
		
		<div class="chapterDiv">
			<span><xsl:text>ID: </xsl:text><xsl:value-of select="@book"/><xsl:text>.</xsl:text><xsl:value-of select="@num"/></span>
			<h3>Chapter <xsl:value-of select="@num"/></h3>
			<xsl:apply-templates/>
		</div>
		
	</xsl:template>


	<xsl:template match="p">
		<p>		
			<xsl:choose>
				<xsl:when test="@highlight='true'"><xsl:attribute name="style">background-color: #c0c0ff</xsl:attribute></xsl:when>
			</xsl:choose>
			<xsl:apply-templates/>
		</p>
	</xsl:template>


	<xsl:template match="s">
		<xsl:choose>
			<xsl:when test="preceding-sibling::s"><xsl:text> </xsl:text></xsl:when>
		</xsl:choose>
		<xsl:apply-templates select="toks"/>
	</xsl:template>


	<xsl:template match="w">
		<xsl:apply-templates/>		
	</xsl:template>


</xsl:stylesheet>
