from lasi_spirometry_reference import predict, score_spirometry


print(predict("M", 60, 165, "fvc"))
print(score_spirometry("M", 60, 165, fev1_l=2.10, fvc_l=2.60))
