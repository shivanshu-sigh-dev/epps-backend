from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, PrescriptionViewSet, DrugInformationViewSet, MultipleImageUploadView, PrescriptionByPatientViewSet, DrugInformationByPrescriptionViewSet, get_prescription_image

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'druginformation', DrugInformationViewSet)

prescription_list = PrescriptionByPatientViewSet.as_view({'get': 'list'})
drug_information_list = DrugInformationByPrescriptionViewSet.as_view({'get': 'list'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('upload-multiple-images/', MultipleImageUploadView.as_view(), name='upload-multiple-images'),
    path('prescriptions/patient/<patient>/', prescription_list, name='prescriptions-by-patient'),
    path('druginformation/prescription/<prescription>/', drug_information_list, name='druginformation-by-prescription'),
    path('prescriptions/image/<prescription_id>/', get_prescription_image, name='get_prescription_image'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
