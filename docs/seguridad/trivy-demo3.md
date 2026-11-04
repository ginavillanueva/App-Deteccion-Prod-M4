# Auditoria Trivy - Demo 3

**Fecha:** 04/11/2026
**Imagen:** app-deteccion:8.3.0
**Herramienta:** Trivy 0.76.1

## Resumen

- HIGH Debian: 45
- HIGH Python: 0
- CRITICAL: 0
- Estado affected: 44 registros
- Estado fix_deferred: 1 registro
- Los 45 hallazgos Debian no tienen version corregida indicada por Trivy.

## Medidas implementadas

- Dockerfile multi-stage.
- Imagen base python:3.11-slim.
- Contenedor ejecutado como usuario no root.
- setuptools==84.2.1 y wheel==0.48.0.
- Hadolint sin advertencias.
- API verificada con HTTP 200.

## Riesgos pendientes

Las vulnerabilidades Debian permanecen abiertas.
No se consideran corregidas ni justificadas individualmente.
Se requiere analizar explotabilidad, exposicion, impacto y mitigacion por CVE.
La ausencia de FixedVersion no demuestra ausencia de riesgo.

## Inventario de hallazgos

| CVE | Paquete | Version instalada | Estado | Version corregida |
|---|---|---|---|---|
| CVE-2026-76642 | bsdutils | 1:2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78408 | bsdutils | 1:2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78409 | bsdutils | 1:2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78410 | bsdutils | 1:2.41.5-0+deb13u1 | affected |  |
| CVE-2026-54369 | libacl1 | 2.3.2-2+b1 | affected |  |
| CVE-2026-76642 | libblkid1 | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78408 | libblkid1 | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78409 | libblkid1 | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78410 | libblkid1 | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-76642 | liblastlog2-2 | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78408 | liblastlog2-2 | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78409 | liblastlog2-2 | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78410 | liblastlog2-2 | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-76642 | libmount1 | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78408 | libmount1 | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78409 | libmount1 | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78410 | libmount1 | 2.41.5-0+deb13u1 | affected |  |
| CVE-2025-69720 | libncursesw6 | 6.5+20250216-2 | affected |  |
| CVE-2026-76642 | libsmartcols1 | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78408 | libsmartcols1 | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78409 | libsmartcols1 | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78410 | libsmartcols1 | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-119373 | libsqlite3-0 | 3.46.1-7+deb13u2 | affected |  |
| CVE-2026-16742 | libsystemd0 | 257.13-1~deb13u1 | affected |  |
| CVE-2025-69720 | libtinfo6 | 6.5+20250216-2 | affected |  |
| CVE-2026-16742 | libudev1 | 257.13-1~deb13u1 | affected |  |
| CVE-2026-76642 | libuuid1 | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78408 | libuuid1 | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78409 | libuuid1 | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78410 | libuuid1 | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-76642 | login | 1:4.16.0-2+really2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78408 | login | 1:4.16.0-2+really2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78409 | login | 1:4.16.0-2+really2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78410 | login | 1:4.16.0-2+really2.41.5-0+deb13u1 | affected |  |
| CVE-2026-76642 | mount | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78408 | mount | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78409 | mount | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78410 | mount | 2.41.5-0+deb13u1 | affected |  |
| CVE-2025-69720 | ncurses-base | 6.5+20250216-2 | affected |  |
| CVE-2025-69720 | ncurses-bin | 6.5+20250216-2 | affected |  |
| CVE-2026-9538 | perl-base | 5.40.1-6+deb13u1 | fix_deferred |  |
| CVE-2026-76642 | util-linux | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78408 | util-linux | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78409 | util-linux | 2.41.5-0+deb13u1 | affected |  |
| CVE-2026-78410 | util-linux | 2.41.5-0+deb13u1 | affected |  |

## Evaluacion de imagen base alternativa

Se analizo python:3.11-slim-bookworm (Debian 12.15) con Trivy 0.76.1.

Resultados de la imagen base alternativa:
- HIGH del sistema operativo: 36.
- HIGH de Python: 2.
- Total HIGH: 38.
- CRITICAL: 2.

La imagen actual de la aplicacion, basada en Debian 13.7, presento:
- HIGH: 45.
- CRITICAL: 0.

Decision: conservar temporalmente python:3.11-slim, basada en Debian 13.

Justificacion: la alternativa presenta dos hallazgos CRITICAL. Ademas, los resultados comparan una imagen base con una imagen de aplicacion, por lo que no constituyen una evaluacion equivalente de ambos despliegues.

Los 45 hallazgos HIGH restantes en la imagen actual continuan pendientes de evaluacion y tratamiento.

## Comprobacion de actualizaciones Debian - 04/11/2026

Se ejecuto apt-get update y apt list --upgradable
sobre la imagen app-deteccion:8.3.0.

Resultado: solamente tzdata tenia una actualizacion disponible:
2026e-0+deb13u1 -> 2026f-0+deb13u1.

No se identificaron otras actualizaciones disponibles en esta consulta.

Esta comprobacion no elimina ni justifica los 45 hallazgos HIGH
pendientes. Se requiere su evaluacion individual.
