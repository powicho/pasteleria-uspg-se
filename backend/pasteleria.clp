;; =============================================================================
;; BASE DE CONOCIMIENTO: PASTELERÍA USPG
;; Dominio: Recomendación y personalización de pasteles por sabores
;; =============================================================================

;; -----------------------------------------------------------------------------
;; 1. DEFTEMPLATES (MOLDE DE HECHOS)
;; -----------------------------------------------------------------------------

(deftemplate componente
   (slot tipo)              ;; bizcocho, relleno, cobertura
   (slot nombre)            ;; limon, chocolate, vainilla, zanahoria, maracuya, 3-leches, etc.
   (slot categoria)         ;; citrico, amargo, dulce, frutal, cremoso, ligera, densa, vegetal
   (slot densidad)          ;; ligera, densa
   (slot contiene-lactosa)  ;; si, no
)

(deftemplate solicitud
   (slot modo)              ;; filtro-general, individual
   (slot restriccion)       ;; ninguna, sin-lactosa
   (slot perfil)            ;; citrico-ligero, chocolatoso-denso, frutal-saludable, dulce-tradicional
)

(deftemplate resultado
   (slot estado)            ;; viable, incompatible, incompleto
   (slot tipo-receta)       ;; exacta, ajustada, error
   (multislot componentes)  ;; lista de componentes seleccionados/recomendados
   (slot mensaje)           ;; mensaje legible para el cliente
   (slot justificacion)     ;; rastro de inferencia que explica la decisión
   (slot regla)             ;; ID de la regla ejecutada
)

;; -----------------------------------------------------------------------------
;; 2. REGLAS DE VALIDACIÓN ESTRUCTURAL Y PRIORITARIA
;; -----------------------------------------------------------------------------

;; R01: Validación de Configuración Incompleta (Salience 180)
;; Si en modo individual falta bizcocho, relleno o cobertura.
(defrule regla-configuracion-incompleta
   (declare (salience 180))
   (solicitud (modo individual))
   (or (not (componente (tipo bizcocho)))
       (not (componente (tipo relleno)))
       (not (componente (tipo cobertura))))
   (not (resultado))
   =>
   (assert (resultado
      (estado incompleto)
      (tipo-receta error)
      (componentes)
      (mensaje "Configuracion incompleta.")
      (justificacion "Todo pastel requiere obligatoriamente una terna completa: 1 Bizcocho, 1 Relleno y 1 Cobertura.")
      (regla "R01-Configuracion-Incompleta")
   ))
)

;; R02: Prioridad Máxima a Restricción Dietética - Sin Lactosa (Salience 150)
;; Si el usuario tiene restricción de lactosa pero seleccionó un ingrediente lácteo.
(defrule regla-conflicto-lactosa
   (declare (salience 150))
   (solicitud (restriccion sin-lactosa))
   (componente (tipo ?tipo) (nombre ?nom) (contiene-lactosa si))
   (not (resultado))
   =>
   (assert (resultado
      (estado incompatible)
      (tipo-receta ajustada)
      (componentes ?nom)
      (mensaje "Conflicto con restriccion alimentaria.")
      (justificacion (str-cat "El componente " ?nom " (" ?tipo ") contiene lactosa. Se activa ajuste forzando sustitucion vegetal."))
      (regla "R02-Prioridad-Restriccion-Lactosa")
   ))
)

;; -----------------------------------------------------------------------------
;; 3. REGLAS DE CONFLICTOS FÍSICOS Y ORGANOLÉPTICOS (Salience 120)
;; -----------------------------------------------------------------------------

;; R03: Conflicto de Densidad y Soporte Físico
(defrule regla-conflicto-densidad
   (declare (salience 120))
   (solicitud (modo individual) (restriccion ninguna))
   (componente (tipo bizcocho) (nombre ?b) (densidad ligera))
   (componente (tipo cobertura) (nombre ?c) (densidad densa))
   (not (resultado))
   =>
   (assert (resultado
      (estado incompatible)
      (tipo-receta ajustada)
      (componentes ?b ?c)
      (mensaje "Conflicto fisico-estructural.")
      (justificacion (str-cat "La cobertura densa " ?c " compromete la estabilidad del bizcocho ligero " ?b ". Se sugiere cobertura ligera."))
      (regla "R03-Conflicto-Densidad-Estructural")
   ))
)

;; R04: Conflicto Organoléptico: Bizcocho Limón con Relleno Cremoso Lácteo
(defrule regla-conflicto-limon-cremoso
   (declare (salience 120))
   (solicitud (modo individual) (restriccion ninguna))
   (componente (tipo bizcocho) (categoria citrico) (nombre ?b))
   (componente (tipo relleno) (categoria cremoso) (nombre ?r))
   (not (resultado))
   =>
   (assert (resultado
      (estado incompatible)
      (tipo-receta ajustada)
      (componentes ?b ?r)
      (mensaje "Conflicto organoleptico acido-graso.")
      (justificacion (str-cat "El sabor citrico de " ?b " choca con el relleno cremoso pesado de " ?r ". Se sugiere relleno frutal (Maracuya/Frutos Rojos)."))
      (regla "R04-Conflicto-Limon-Cremoso")
   ))
)

;; -----------------------------------------------------------------------------
;; 4. REGLAS DE MODO FILTRO GENERAL (Salience 100)
;; -----------------------------------------------------------------------------

;; R05: Filtro General - Perfil Cítrico Ligero
(defrule regla-filtro-citrico-ligero
   (declare (salience 100))
   (solicitud (modo filtro-general) (restriccion ninguna) (perfil citrico-ligero))
   (not (resultado))
   =>
   (assert (resultado
      (estado viable)
      (tipo-receta exacta)
      (componentes limon maracuya merengue-italiano)
      (mensaje "Pastel Citrico Ligero: Bizcocho de Limon con Curd de Maracuya y Merengue Italiano.")
      (justificacion "Combinacion ideal para dulzor bajo y perfil refrescante citrico.")
      (regla "R05-Filtro-Citrico-Ligero")
   ))
)

;; R06: Filtro General - Perfil Chocolatoso Denso
(defrule regla-filtro-chocolatoso-denso
   (declare (salience 100))
   (solicitud (modo filtro-general) (restriccion ninguna) (perfil chocolatoso-denso))
   (not (resultado))
   =>
   (assert (resultado
      (estado viable)
      (tipo-receta exacta)
      (componentes chocolate-humedo mermelada-cereza ganache)
      (mensaje "Pastel Selva Negra: Bizcocho humedo de cacao, relleno de cereza y cobertura de ganache.")
      (justificacion "Estructura densa con equilibrio entre amargor de cacao y dulzor de ganache.")
      (regla "R06-Filtro-Chocolatoso-Denso")
   ))
)

;; R07: Filtro General - Sin Lactosa / Frutal Saludable
(defrule regla-filtro-sin-lactosa-frutal
   (declare (salience 100))
   (solicitud (modo filtro-general) (restriccion sin-lactosa))
   (not (resultado))
   =>
   (assert (resultado
      (estado viable)
      (tipo-receta exacta)
      (componentes vainilla-vegetal frutos-rojos crema-vegetal)
      (mensaje "Pastel Frutal Libre de Lactosa: Bizcocho de vainilla vegetal, relleno frutos rojos y crema vegetal.")
      (justificacion "100% libre de derivados lacteos con balance frutal.")
      (regla "R07-Filtro-Sin-Lactosa-Frutal")
   ))
)

;; -----------------------------------------------------------------------------
;; 5. REGLA DE SELECCIÓN INDIVIDUAL VIABLE (Salience 50)
;; -----------------------------------------------------------------------------

;; R08: Confirmación de Selección Individual Viable (Receta Exacta)
(defrule regla-seleccion-individual-viable
   (declare (salience 50))
   (solicitud (modo individual))
   (componente (tipo bizcocho) (nombre ?b))
   (componente (tipo relleno) (nombre ?r))
   (componente (tipo cobertura) (nombre ?c))
   (not (resultado))
   =>
   (assert (resultado
      (estado viable)
      (tipo-receta exacta)
      (componentes ?b ?r ?c)
      (mensaje (str-cat "Combinacion personalizada aprobada: " ?b " + " ?r " + " ?c))
      (justificacion "La terna cumple con la integridad estructural, armonía organoléptica y restricciones.")
      (regla "R08-Seleccion-Individual-Viable")
   ))
)