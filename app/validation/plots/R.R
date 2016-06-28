plot(tfidf, xlab="Number of words", ylab="Recall", main="Recall vs Number of words - WebIndex", cex=.1, col="blue")
lines(`tfidf2`, col="red")
lines(`tfidf2stem`, col="purple")
lines(`tfidf3`, col="orange")
lines(`tfidfstem`, col="yellow")
lines(`tfidf2sw`, col="brown")
lines(random1, col="black")
lines(random2, col="black")
lines(random3, col="black")
legend("center", 'left', 
       legend=c(
         "tf*idf/norms - 5701","tf^2*idf*idl/norms+boost - 6171", 
         "tf^2*idf/norms+boost - 6149", 
         "stemming - tf^2*idf*idl/norms+boost - 4064", 
         "stemming - tf*idf/norms - 3733",
         "stop words - tf^2*idf*idl/norms+boost - 5912",
         "Random (3x) - ~3500"), 
       col=c("blue", "red", "orange", "purple", "yellow", "brown", "black"), lwd=3)
