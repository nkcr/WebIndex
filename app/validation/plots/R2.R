plot(tfidf, xlab="Number of words", ylab="Precision", main="Precision vs Number of words - WebIndex", cex=.1, col="blue")
lines(`tfidf2`, col="red")
lines(`tfidf2stem`, col="purple")
lines(`tfidf3`, col="orange")
lines(`tfidfstem`, col="yellow")
lines(`tfidf2sw`, col="brown")
lines(random1, col="black")
lines(random2, col="black")
lines(random3, col="black")
legend("topright", 
       legend=c(
         "tf*idf/norms - 1105",
         "tf^2*idf*idl/norms+boost - 1307", 
         "tf^2*idf/norms+boost - 1254", 
         "stemming - tf^2*idf*idl/norms+boost - 1113", 
         "stemming - tf*idf/norms - 947",
         "stop words - tf^2*idf*idl/norms+boost - 1322",
         "Random (3x) - ~290"), 
       col=c("blue", "red", "orange", "purple", "yellow", "brown", "black"), lwd=3)
